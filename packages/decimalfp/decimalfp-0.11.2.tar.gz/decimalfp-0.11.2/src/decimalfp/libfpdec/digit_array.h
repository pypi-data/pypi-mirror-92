/*
------------------------------------------------------------------------------
Name:        digit_array.h

Author:      Michael Amrhein (michael@adrhinum.de)

Copyright:   (c) 2020 ff. Michael Amrhein
License:     This program is part of a larger application or library.
             For license details please read the file LICENSE provided
             together with the application or library.
------------------------------------------------------------------------------
$Source: src/decimalfp/libfpdec/digit_array.h $
$Revision: 2020-10-10T09:34:22+02:00 $
*/


#ifndef FPDEC_DIGIT_ARRAY_H
#define FPDEC_DIGIT_ARRAY_H

#include "common.h"
#include "helper_macros.h"
#include "mem.h"
#include "rounding.h"


/*****************************************************************************
*  Macros
*****************************************************************************/

#define MAX_DIGIT 9999999999999999999UL     // RADIX - 1

/*****************************************************************************
*  Functions
*****************************************************************************/

// Constructors

fpdec_digit_array_t *
digits_copy(const fpdec_digit_array_t *src, fpdec_n_digits_t n_shift,
            fpdec_n_digits_t n_add_leading_zeros);

error_t
digits_from_dec_coeff_exp(fpdec_digit_array_t **digit_array, fpdec_exp_t *exp,
                          size_t n_dec_digits, const dec_digit_t *coeff,
                          int64_t dec_exp);

error_t
digits_from_digits(fpdec_digit_array_t **digit_array,
                   const fpdec_digit_t *digits, size_t n_digits);

// Tests

static inline bool
digits_all_zero(fpdec_digit_t *digits, fpdec_n_digits_t n) {
    for (fpdec_digit_t *digit = digits; digit < digits + n; ++digit)
        if (*digit != 0)
            return false;
    return true;
}

// Normalization

fpdec_n_digits_t
digits_eliminate_trailing_zeros(fpdec_digit_array_t *digit_array);

// Rounding

bool
digits_round(fpdec_digit_array_t *digit_array, fpdec_sign_t sign,
             size_t n_dec_shift, enum FPDEC_ROUNDING_MODE rounding);

// Comparison

int
digits_cmp(fpdec_digit_t *x_digits, fpdec_n_digits_t x_n_digits,
           fpdec_digit_t *y_digits, fpdec_n_digits_t y_n_digits);

// Basic arithmetic operations

bool
digits_iadd_digit(fpdec_digit_array_t *x, fpdec_digit_t y);

void
digits_iadd_digits(fpdec_digit_array_t *x, const fpdec_digit_array_t *y);

void
digits_isub_digits(fpdec_digit_array_t *x, const fpdec_digit_array_t *y);

void
digits_imul_digit(fpdec_digit_array_t *x, fpdec_digit_t y);

fpdec_digit_array_t *
digits_mul(const fpdec_digit_array_t *x, const fpdec_digit_array_t *y);

fpdec_digit_array_t *
digits_div_digit(const fpdec_digit_array_t *x,
                 const fpdec_n_digits_t x_n_shift,
                 const fpdec_digit_t y, fpdec_digit_t *rem);

fpdec_digit_array_t *
digits_divmod(const fpdec_digit_array_t *x, const fpdec_n_digits_t x_n_shift,
              const fpdec_digit_array_t *y, const fpdec_n_digits_t y_n_shift,
              fpdec_digit_array_t **rem);

fpdec_digit_array_t *
digits_div_max_prec(const fpdec_digit_array_t *x,
                    const fpdec_digit_array_t *y,
                    int *exp);

fpdec_digit_array_t *
digits_div_limit_prec(const fpdec_digit_array_t *x, const fpdec_n_digits_t x_n_shift,
                      const fpdec_digit_array_t *y, const fpdec_n_digits_t y_n_shift);

#endif //FPDEC_DIGIT_ARRAY_H
