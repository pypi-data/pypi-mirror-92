/* ---------------------------------------------------------------------------
Name:        format_spec.c

Author:      Michael Amrhein (michael@adrhinum.de)

Copyright:   (c) 2020 ff. Michael Amrhein
License:     This program is part of a larger application. For license
             details please read the file LICENSE.TXT provided together
             with the application.
------------------------------------------------------------------------------
$Source: src/decimalfp/libfpdec/format_spec.c $
$Revision: 2020-11-23T11:47:23+01:00 $
*/

#include <assert.h>
#include <ctype.h>
#include <locale.h>
#include <memory.h>
#include <stdbool.h>
#include "format_spec.h"

/*****************************************************************************
*  Constants
*****************************************************************************/

const format_spec_t DFLT_FORMAT = {
    .fill = {1, " "},
    .align = '>',
    .sign = '-',
    .min_width = 0,
    .thousands_sep = {0, ""},
    .grouping = {3, 0, 0, 0, 0},
    .decimal_point = {1, "."},
    .precision = SIZE_MAX,
    .type = 'f'
};

const utf8c_t no_fill = {0, ""};

/*****************************************************************************
*  Functions
*****************************************************************************/

// Format string:
// [[fill]align][sign][0][min_width][,][.precision][type]
int
parse_format_spec(format_spec_t *spec, const uint8_t *fmt) {
    const uint8_t *cp = fmt;
    bool got_fill = false;
    int t;
    size_t n;

    *spec = DFLT_FORMAT;

    // check for fill character
    t = utf8c_len(cp);
    if (t <= 0)
        return t;
    n = (size_t)t;
    assert(n <= 4);
    if (*(cp + n) == '<' || *(cp + n) == '>' || *(cp + n) == '=' ||
        *(cp + n) == '^') {
        // fill + align
        memcpy(spec->fill.bytes, cp, n);
        spec->fill.n_bytes = n;
        cp += n;
        spec->align = *cp++;
        got_fill = true;
    }
    else {
        // align without fill?
        if (*cp == '<' || *cp == '>' || *cp == '=' || *cp == '^')
            spec->align = *cp++;
    }

    // sign formatting
    if (*cp == '-' || *cp == '+' || *cp == ' ')
        spec->sign = *cp++;

    // zero padding
    if (*cp == '0') {
        if (!got_fill) {                // fill overrules zeropad
            spec->fill.bytes[0] = '0';
            spec->fill.n_bytes = 1;
            spec->align = '=';         // zeropad overrules align
        }
        cp++;
    }

    // minimum total field width
    if (isdigit(*cp)) {
        size_t mw;
        if (*cp == '0')
            return -1;
        spec->min_width = *cp++ - '0';
        while (isdigit(*cp)) {
            mw = spec->min_width;
            spec->min_width = mw * 10 + (*cp++ - '0');
            if (spec->min_width < mw)
                return -1;
        }
    }

    // thousands seperator
    if (*cp == ',') {
        cp++;
        spec->thousands_sep.bytes[0] = ',';
        spec->thousands_sep.n_bytes = 1;
    }

    // decimal point and number of fractional digits
    if (*cp == '.') {
        size_t p;
        cp++;
        if (!isdigit(*cp))
            return -1;
        spec->precision = *cp++ - '0';
        while (isdigit(*cp)) {
            p = spec->precision;
            spec->precision = p * 10 + (*cp++ - '0');
            if (spec->precision < p)
                return -1;
        }
    }

    // format type
    if (*cp == 'f' || *cp == 'F' || *cp == 'n' || *cp == '%')
        spec->type = *cp++;

    // check end of format
    if (*cp != '\0')
        return -1;

    // no fill and align without min_width
    if (spec->min_width == 0) {
        spec->fill = no_fill;
        spec->align = '<';
    }

    // set locale specific params if requested
    if (spec->type == 'n') {
        struct lconv *lc = localeconv();
        if (spec->thousands_sep.n_bytes != 0) {
            n = strlen(lc->thousands_sep);
            if (n > 4)
                return -2;
            if (n > 0)
                memcpy(spec->thousands_sep.bytes, lc->thousands_sep, n);
            spec->thousands_sep.n_bytes = n;
        }
        n = strlen(lc->grouping);
        if (n >= sizeof(spec->grouping))
            return -2;
        for (size_t i = 0; i < n; ++i)
            spec->grouping[i] = lc->grouping[i];
        spec->grouping[n] = 0;
        n = strlen(lc->decimal_point);
        if (n == 0 || n > 4)
            return -2;
        memcpy(spec->decimal_point.bytes, lc->decimal_point, n);
        spec->decimal_point.n_bytes = n;
    }

    return 0;
}
