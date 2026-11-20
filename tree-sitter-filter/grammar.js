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
      choice($.string, $.number),
    ),
    and_expression: $ => seq($._expr, 'and', $._expr),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,

    _expr: $ => choice($.comparison, $.and_expression, $.or_expression),
    or_expression: $ => seq($._expr, 'or', $._expr),
  }
});
