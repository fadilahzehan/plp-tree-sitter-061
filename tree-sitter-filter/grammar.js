/**
 * @file Filter grammar for tree-sitter
 * @author zehan <fadilahzehan@gmail.com>
 * @license MIT
 */

module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  rules: {
    query: $ => $.comparison,
    comparison: $ => seq($.identifier, '=', $.string),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
  }
});
