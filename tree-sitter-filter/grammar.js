/**
 * @file Filter grammar for tree-sitter
 * @author zehan <fadilahzehan@gmail.com>
 * @license MIT
 */

module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  word: $ => $.identifier,
  rules: {
    query: $ => $._expr,
    _expr: $ => choice($.comparison, $.and_expression),
    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='),
      choice($._value, $.number),
    ),
    and_expression: $ => seq($._expr, 'and', $._expr),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,

    _expr: $ => choice($.comparison, $.and_expression, $.or_expression),
    or_expression: $ => prec.left(1, seq($._expr, 'or', $._expr)),
    and_expression: $ => prec.left(2, seq($._expr, 'and', $._expr)),

    _expr: $ => choice($.comparison, $.and_expression, $.or_expression, $.parenthesized),
    parenthesized: $ => seq('(', $._expr, ')'),

    _expr: $ => choice($.comparison, $.and_expression, $.or_expression, $.not_expression, $.parenthesized),
    not_expression: $ => prec(3, seq('not', $._expr)),
    _value: $ => choice($.string, $.number, $.boolean),
    boolean: $ => choice('true', 'false'),
  }
});
