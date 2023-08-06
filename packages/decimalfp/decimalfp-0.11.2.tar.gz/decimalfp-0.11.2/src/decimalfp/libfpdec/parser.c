/* ---------------------------------------------------------------------------
Name:        parser.c

Author:      Michael Amrhein (michael@adrhinum.de)

Copyright:   (c) 2020 ff. Michael Amrhein
License:     This program is part of a larger application. For license
             details please read the file LICENSE.TXT provided together
             with the application.
------------------------------------------------------------------------------
$Source: src/decimalfp/libfpdec/parser.c $
$Revision: 2020-11-23T11:47:23+01:00 $
*/

#include <ctype.h>
#include <stddef.h>

#include "compiler_macros.h"
#include "parser.h"

/*****************************************************************************
*  Functions
*****************************************************************************/

static inline void
fill_in_digits(dec_repr_t *dec_repr, const char *dec_chars,
               const size_t n_dec_digits) {
    const char *curr_char = dec_chars;
    dec_digit_t *curr_digit = dec_repr->coeff + dec_repr->n_dec_digits;
    for (size_t i = 0; i < n_dec_digits; ++i) {
        *curr_digit = *curr_char - '0';
        curr_char++;
        curr_digit++;
    }
    dec_repr->n_dec_digits += n_dec_digits;
}

// parse for a Decimal
// [+|-]<int>[.<frac>][<e|E>[+|-]<exp>] or
// [+|-].<frac>[<e|E>[+|-]<exp>].
error_t
parse_ascii_dec_literal(dec_repr_t *result, const char *literal) {
    const char *curr_char = literal;
    const char *int_part = NULL;
    const char *signif_int_part = NULL;
    ptrdiff_t len_int_part;
    const char *frac_part = NULL;
    ptrdiff_t len_frac_part = 0;
    int64_t t;

    while isspace(*curr_char) {
        curr_char++;
    }
    if (*curr_char == 0) return FPDEC_INVALID_DECIMAL_LITERAL;

    result->negative = false;
    result->exp = 0;
    result->n_dec_digits = 0;

    switch (*curr_char) {
        case '-':
            result->negative = true;
            FALLTHROUGH;
        case '+':
            curr_char++;
    }
    int_part = curr_char;
    while (*curr_char == '0') {
        curr_char++;
    }
    signif_int_part = curr_char;
    while (isdigit(*curr_char)) {
        curr_char++;
    }
    len_int_part = curr_char - signif_int_part;
    if (*curr_char == '.') {
        curr_char++;
        frac_part = curr_char;
        while (isdigit(*curr_char)) {
            curr_char++;
        }
        len_frac_part = curr_char - frac_part;
    }
    if (len_int_part == 0 && len_frac_part == 0) {
        if (*int_part == '0') {
            signif_int_part = int_part;
            len_int_part = 1;
        }
        else
            return FPDEC_INVALID_DECIMAL_LITERAL;
    }
    if (*curr_char == 'e' || *curr_char == 'E') {
        int8_t sign = 1;
        int64_t exp = 0;
        curr_char++;
        switch (*curr_char) {
            case '-':
                sign = -1;
                FALLTHROUGH;
            case '+':
                curr_char++;
                break;
            default:
                if (!isdigit(*curr_char))
                    return FPDEC_INVALID_DECIMAL_LITERAL;
        }
        while isdigit(*curr_char) {
            t = exp;
            exp = exp * 10 + (*curr_char - '0');
            if (exp < t)    // overflow occured!
                return FPDEC_EXP_LIMIT_EXCEEDED;
            curr_char++;
        }
        result->exp = sign * exp;
    }
    while isspace(*curr_char) {
        curr_char++;
    }
    if (*curr_char != 0)
        return FPDEC_INVALID_DECIMAL_LITERAL;
    t = result->exp;
    result->exp -= len_frac_part;
    if (result->exp > t)    // overflow occured!
        return FPDEC_EXP_LIMIT_EXCEEDED;
    if (result->exp > 0) {
        t = CEIL(result->exp, DEC_DIGITS_PER_DIGIT);
        if (t > FPDEC_MAX_EXP)
            return FPDEC_EXP_LIMIT_EXCEEDED;
    }
    if (-result->exp > FPDEC_MAX_DEC_PREC)
        return FPDEC_PREC_LIMIT_EXCEEDED;
    fill_in_digits(result, signif_int_part, len_int_part);
    fill_in_digits(result, frac_part, len_frac_part);
    return FPDEC_OK;
}
