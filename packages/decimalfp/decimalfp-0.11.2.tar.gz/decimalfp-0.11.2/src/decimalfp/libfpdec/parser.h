/* ---------------------------------------------------------------------------
Name:        parser.h

Author:      Michael Amrhein (michael@adrhinum.de)

Copyright:   (c) 2020 ff. Michael Amrhein
License:     This program is part of a larger application. For license
             details please read the file LICENSE.TXT provided together
             with the application.
------------------------------------------------------------------------------
$Source: src/decimalfp/libfpdec/parser.h $
$Revision: 2020-10-10T09:34:22+02:00 $
*/

#ifndef FPDEC_PARSER_H
#define FPDEC_PARSER_H

#include "common.h"
#include "helper_macros.h"
#include "uint64_math.h"


/*****************************************************************************
*  Types
*****************************************************************************/

#define COEFF_SIZE_THRESHOLD 255

// represent decimal number as (negative ? -1 : 1) * coeff * pow(10, exp)
typedef struct {
    bool negative;
    int64_t exp;
    size_t n_dec_digits;
    dec_digit_t coeff[COEFF_SIZE_THRESHOLD];
} dec_repr_t;

/*****************************************************************************
*  Functions
*****************************************************************************/

error_t
parse_ascii_dec_literal(dec_repr_t *result, const char *literal);

#endif //FPDEC_PARSER_H
