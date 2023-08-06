# -*- coding: utf-8 -*-
# This file is part of the lib3to6 project
# https://gitlab.com/mbarkhau/lib3to6
#
# Copyright (c) 2019-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import ast
import itertools
import typing as typ
zip = getattr(itertools, 'izip', zip)
from . import common
from . import fixer_base as fb
AstStr = getattr(ast, 'Str', ast.Constant)
ArgUnpackNodes = ast.Call, ast.List, ast.Tuple, ast.Set
KwArgUnpackNodes = ast.Call, ast.Dict


def _is_dict_call(node):
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name
        ) and node.func.id == 'dict'


def _has_stararg_g12n(node):
    if isinstance(node, ast.Call):
        elts = node.args
    elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        elts = node.elts
    else:
        raise TypeError('Unexpected node: {0}'.format(node))
    has_starred_arg = False
    for arg in elts:
        if has_starred_arg:
            return True
        has_starred_arg = isinstance(arg, ast.Starred)
    return False


def _has_starstarargs_g12n(node):
    if isinstance(node, ast.Call):
        has_kwstarred_arg = False
        for keyword in node.keywords:
            if has_kwstarred_arg:
                return True
            has_kwstarred_arg = keyword.arg is None
        return False
    elif isinstance(node, ast.Dict):
        has_kwstarred_arg = False
        for key in node.keys:
            if has_kwstarred_arg:
                return True
            has_kwstarred_arg = key is None
        return False
    else:
        raise TypeError('Unexpected node: {0}'.format(node))


def _node_with_elts(node, new_elts):
    if isinstance(node, ast.Call):
        node.args = new_elts
        return node
    elif isinstance(node, ast.List):
        return ast.List(elts=new_elts)
    elif isinstance(node, ast.Set):
        return ast.Set(elts=new_elts)
    elif isinstance(node, ast.Tuple):
        return ast.Tuple(elts=new_elts)
    else:
        raise TypeError('Unexpected node type {0}'.format(type(node)))


def _node_with_binop(node, binop):
    if isinstance(node, ast.Call):
        node.args = [ast.Starred(value=binop, ctx=ast.Load())]
        return node
    elif isinstance(node, ast.List):
        return binop
    elif isinstance(node, ast.Set):
        return ast.Call(func=ast.Name(id='set', ctx=ast.Load()), args=[
            binop], keywords=[])
    elif isinstance(node, ast.Tuple):
        return ast.Call(func=ast.Name(id='tuple', ctx=ast.Load()), args=[
            binop], keywords=[])
    else:
        raise TypeError('Unexpected node type {0}'.format(type(node)))


def _is_stmtlist(nodelist):
    return isinstance(nodelist, list) and all(isinstance(n, ast.stmt) for n in
        nodelist)


def _iter_walkable_fields(node):
    for field_name, field_node in ast.iter_fields(node):
        if isinstance(field_node, ast.arguments):
            continue
        if isinstance(field_node, ast.expr_context):
            continue
        if isinstance(field_node, common.LeafNodeTypes):
            continue
        yield field_name, field_node


def _expand_stararg_g12n(node):
    """Convert fn(*x, *[1, 2], z) -> fn(*(list(x) + [1, 2, z])).

    NOTE (mb 2018-07-06): The goal here is to create an expression
      which is a list, by either creating
        1. a single list node
        2. a BinOp tree where all of the node.elts/args
            are converted to lists and concatenated.
    """
    if isinstance(node, ast.Call):
        elts = node.args
    elif isinstance(node, common.ContainerNodes):
        elts = node.elts
    else:
        raise TypeError('Unexpected node: {0}'.format(node))
    operands = [ast.List(elts=[])]
    for elt in elts:
        tail_list = operands[-1]
        assert isinstance(tail_list, ast.List)
        tail_elts = tail_list.elts
        if not isinstance(elt, ast.Starred):
            tail_elts.append(elt)
            continue
        val = elt.value
        if isinstance(val, common.ContainerNodes):
            tail_elts.extend(val.elts)
            continue
        new_val_node = ast.Call(func=ast.Name(id='list', ctx=ast.Load()),
            args=[val], keywords=[])
        if len(tail_elts) == 0:
            operands[-1] = new_val_node
        else:
            operands.append(new_val_node)
        operands.append(ast.List(elts=[]))
    tail_list = operands[-1]
    assert isinstance(tail_list, ast.List)
    if len(tail_list.elts) == 0:
        operands = operands[:-1]
    if len(operands) == 1:
        tail_list = operands[0]
        assert isinstance(tail_list, ast.List)
        return _node_with_elts(node, tail_list.elts)
    if len(operands) > 1:
        binop = ast.BinOp(left=operands[0], op=ast.Add(), right=operands[1])
        for operand in operands[2:]:
            binop = ast.BinOp(left=binop, op=ast.Add(), right=operand)
        return _node_with_binop(node, binop)
    raise RuntimeError('This should not happen')


class UnpackingGeneralizationsFixer(fb.FixerBase):
    version_info = common.VersionInfo(apply_since='2.0', apply_until='3.4')

    def expand_starstararg_g12n(self, node):
        chain_values = []
        chain_val = None
        if isinstance(node, ast.Dict):
            for key, val in zip(node.keys, node.values):
                if key is None:
                    chain_val = val
                else:
                    chain_val = ast.Dict(keys=[key], values=[val])
                chain_values.append(chain_val)
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg is None:
                    chain_val = keyword.value
                else:
                    chain_val = ast.Dict(keys=[AstStr(s=keyword.arg)],
                        values=[keyword.value])
                chain_values.append(chain_val)
        else:
            raise TypeError('Unexpected node type {0}'.format(node))
        collapsed_chain_values = []
        for chain_val in chain_values:
            if len(collapsed_chain_values) == 0:
                collapsed_chain_values.append(chain_val)
            else:
                prev_chain_val = collapsed_chain_values[-1]
                if isinstance(chain_val, ast.Dict) and isinstance(
                    prev_chain_val, ast.Dict):
                    for key, val in zip(chain_val.keys, chain_val.values):
                        prev_chain_val.keys.append(key)
                        prev_chain_val.values.append(val)
                else:
                    collapsed_chain_values.append(chain_val)
        assert len(collapsed_chain_values) > 0
        if len(collapsed_chain_values) == 1:
            collapsed_chain_value = collapsed_chain_values[0]
            if isinstance(node, ast.Dict):
                return collapsed_chain_value
            elif isinstance(node, ast.Call):
                node_func = node.func
                node_args = node.args
                if isinstance(node_func, ast.Name) and node_func.id == 'dict':
                    return collapsed_chain_value
                else:
                    return ast.Call(func=node_func, args=node_args,
                        keywords=[ast.keyword(arg=None, value=
                        collapsed_chain_value)])
            else:
                raise TypeError('Unexpected node type {0}'.format(node))
        else:
            assert isinstance(node, ast.Call)
            self.required_imports.add(common.ImportDecl('itertools', None,
                None))
            chain_args = []
            for val in chain_values:
                items_func = ast.Attribute(value=val, attr='items', ctx=ast
                    .Load())
                chain_args.append(ast.Call(func=items_func, args=[],
                    keywords=[]))
            value_node = ast.Call(func=ast.Name(id='dict', ctx=ast.Load()),
                args=[ast.Call(func=ast.Attribute(value=ast.Name(id=
                'itertools', ctx=ast.Load()), attr='chain', ctx=ast.Load()),
                args=chain_args, keywords=[])], keywords=[])
            node.keywords = [ast.keyword(arg=None, value=value_node)]
        return node

    def visit_expr(self, node):
        new_node = node
        if isinstance(node, ArgUnpackNodes) and _has_stararg_g12n(node):
            new_node = _expand_stararg_g12n(new_node)
        if isinstance(node, KwArgUnpackNodes) and _has_starstarargs_g12n(node):
            new_node = self.expand_starstararg_g12n(new_node)
        return new_node

    def walk_stmtlist(self, stmtlist):
        assert _is_stmtlist(stmtlist)
        new_stmts = []
        for stmt in stmtlist:
            new_stmt = self.walk_stmt(stmt)
            new_stmts.append(new_stmt)
        return new_stmts

    def walk_node(self, node):
        if isinstance(node, common.LeafNodeTypes):
            return node
        for field_name, field_node in _iter_walkable_fields(node):
            if isinstance(field_node, ast.AST):
                new_node = self.walk_node(field_node)
                setattr(node, field_name, new_node)
            elif isinstance(field_node, list):
                new_field_node = []
                new_sub_node = None
                for sub_node in field_node:
                    if isinstance(sub_node, common.LeafNodeTypes):
                        new_sub_node = sub_node
                    elif isinstance(sub_node, ast.AST):
                        new_sub_node = self.walk_node(sub_node)
                    else:
                        new_sub_node = sub_node
                    new_field_node.append(new_sub_node)
                setattr(node, field_name, new_field_node)
        if not isinstance(node, ast.expr):
            return node
        new_expr_node = self.visit_expr(node)
        if isinstance(new_expr_node, ast.Call):
            is_single_dict_splat = _is_dict_call(new_expr_node) and len(
                new_expr_node.args) == 0 and len(new_expr_node.keywords
                ) == 1 and new_expr_node.keywords[0].arg is None
            if is_single_dict_splat:
                keyword_node = new_expr_node.keywords[0]
                if _is_dict_call(keyword_node.value) or isinstance(keyword_node
                    .value, ast.Dict):
                    return keyword_node.value
        return new_expr_node

    def walk_stmt(self, node):
        assert not _is_stmtlist(node)
        for field_name, field_node in _iter_walkable_fields(node):
            if _is_stmtlist(field_node):
                old_field_nodelist = field_node
                new_field_nodelist = self.walk_stmtlist(old_field_nodelist)
                setattr(node, field_name, new_field_nodelist)
            elif isinstance(field_node, ast.stmt):
                new_stmt = self.walk_stmt(field_node)
                setattr(node, field_name, new_stmt)
            elif isinstance(field_node, ast.AST):
                new_node = self.walk_node(field_node)
                setattr(node, field_name, new_node)
            elif isinstance(field_node, list):
                new_field_node = []
                new_sub_node = None
                for sub_node in field_node:
                    if isinstance(sub_node, common.LeafNodeTypes):
                        new_sub_node = sub_node
                    elif isinstance(sub_node, ast.AST):
                        new_sub_node = self.walk_node(sub_node)
                    else:
                        new_sub_node = sub_node
                    new_field_node.append(new_sub_node)
                setattr(node, field_name, new_field_node)
            else:
                continue
        return node

    def __call__(self, ctx, tree):
        tree.body = self.walk_stmtlist(tree.body)
        return tree
