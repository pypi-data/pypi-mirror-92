/*
------------------------------------------------------------------------------
Name:        rounding_helper.h

Author:      Michael Amrhein (michael@adrhinum.de)

Copyright:   (c) 2020 ff. Michael Amrhein
License:     This program is part of a larger application or library.
             For license details please read the file LICENSE provided
             together with the application or library.
------------------------------------------------------------------------------
$Source: src/decimalfp/libfpdec/rounding_helper.h $
$Revision: 2020-11-23T11:47:23+01:00 $
*/

#ifndef FPDEC_ROUNDING_HELPER_H
#define FPDEC_ROUNDING_HELPER_H

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

#include "compiler_macros.h"
#include "common.h"
#include "rounding.h"
#include "basemath.h"


static inline fpdec_digit_t UNUSED
round_qr(fpdec_sign_t sign, fpdec_digit_t quot, fpdec_digit_t rem, bool delta,
         fpdec_digit_t divisor, enum FPDEC_ROUNDING_MODE rounding) {
    const uint64_t max_tie = 0x8000000000000000;
    fpdec_digit_t tie;

    assert(rem > 0 || delta);
    // divisor == 0 means divisor == 2^64
    assert(divisor == 0 || rem < divisor);
    assert(0 <= rounding && rounding <= FPDEC_MAX_ROUNDING_MODE);

    if (rounding == FPDEC_ROUND_DEFAULT) {
        rounding = fpdec_get_default_rounding_mode();
    }

    switch (rounding) {
        case FPDEC_ROUND_05UP:
            // Round down unless last digit is 0 or 5
            if (quot % 5 == 0)
                return 1;
            break;
        case FPDEC_ROUND_CEILING:
            // Round towards Infinity (i. e. not towards 0 if non-negative)
            if (sign >= 0)
                return 1;
            break;
        case FPDEC_ROUND_DOWN:
            // Round towards 0 (aka truncate)
            break;
        case FPDEC_ROUND_FLOOR:
            // Round towards -Infinity (i.e. not towards 0 if negative)
            if (sign < 0)
                return 1;
            break;
        case FPDEC_ROUND_HALF_DOWN:
            // Round 5 down, rest to nearest
            tie = divisor > 0 ? divisor >> 1U : max_tie;
            if (rem > tie || (rem == tie && delta)) {
                return 1;
            }
            break;
        case FPDEC_ROUND_HALF_EVEN:
            // Round 5 to nearest even, rest to nearest
            tie = divisor > 0 ? divisor >> 1UL : max_tie;
            if (rem > tie || (rem == tie && (delta || quot % 2 != 0)))
                return 1;
            break;
        case FPDEC_ROUND_HALF_UP:
            // Round 5 up (away from 0), rest to nearest
            tie = divisor > 0 ? divisor >> 1UL : max_tie;
            if (rem >= tie)
                return 1;
            break;
        case FPDEC_ROUND_UP:
            // Round away from 0
            return 1;
        default:
            return 0;
    }
    // fall-through: round towards 0
    return 0;
}

fpdec_digit_t
round_to_multiple(fpdec_sign_t sign, fpdec_digit_t num, bool delta,
                  fpdec_digit_t quant, enum FPDEC_ROUNDING_MODE rounding);

static inline bool UNUSED
round_u128(fpdec_sign_t sign, uint128_t *quot, uint128_t *rem,
           uint128_t *divisor, enum FPDEC_ROUNDING_MODE rounding) {
    uint128_t tie;
    int cmp;

    assert(U128P_NE_ZERO(rem));
    assert(u128_cmp(*rem, *divisor) < 0);
    assert(0 <= rounding && rounding <= FPDEC_MAX_ROUNDING_MODE);

    if (rounding == FPDEC_ROUND_DEFAULT) {
        rounding = fpdec_get_default_rounding_mode();
    }

    switch (rounding) {
        case FPDEC_ROUND_05UP:
            // Round down unless last digit is 0 or 5
            if (U128P_LO(quot) % 5 == 0)
                return true;
            break;
        case FPDEC_ROUND_CEILING:
            // Round towards Infinity (i. e. not towards 0 if non-negative)
            if (sign >= 0)
                return true;
            break;
        case FPDEC_ROUND_DOWN:
            // Round towards 0 (aka truncate)
            break;
        case FPDEC_ROUND_FLOOR:
            // Round towards -Infinity (i.e. not towards 0 if negative)
            if (sign < 0)
                return true;
            break;
        case FPDEC_ROUND_HALF_DOWN:
            // Round 5 down, rest to nearest
            tie = u128_shift_right(divisor, 1UL);
            if (u128_cmp(*rem, tie) > 0)
                return true;
            break;
        case FPDEC_ROUND_HALF_EVEN:
            // Round 5 to nearest even, rest to nearest
            tie = u128_shift_right(divisor, 1UL);
            cmp = u128_cmp(*rem, tie);
            if (cmp > 0 || (cmp == 0 && U128P_LO(divisor) % 2 == 0 &&
                U128P_LO(quot) % 2 != 0))
                return true;
            break;
        case FPDEC_ROUND_HALF_UP:
            // Round 5 up (away from 0), rest to nearest
            tie = u128_shift_right(divisor, 1UL);
            cmp = u128_cmp(*rem, tie);
            if (cmp > 0 || (cmp == 0 && U128P_LO(divisor) % 2 == 0))
                return true;
            break;
        case FPDEC_ROUND_UP:
            // Round away from 0
            return true;
        default:
            return false;
    }
    // fall-through: round towards 0
    return false;
}

#ifdef __cplusplus
}
#endif // __cplusplus

#endif //FPDEC_ROUNDING_HELPER_H
