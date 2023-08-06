/* ---------------------------------------------------------------------------
Name:        mem.h

Author:      Michael Amrhein (michael@adrhinum.de)

Copyright:   (c) 2020 ff. Michael Amrhein
License:     This program is part of a larger application. For license
             details please read the file LICENSE.TXT provided together
             with the application.
------------------------------------------------------------------------------
$Source: src/decimalfp/libfpdec/mem.h $
$Revision: 2020-11-23T11:47:23+01:00 $
*/

#ifndef FPDEC_MEM_H
#define FPDEC_MEM_H

#include <malloc.h>
#include "compiler_macros.h"

typedef void * (*mem_alloc_func)(size_t num, size_t size);
typedef void (*mem_free_func)(void *);

static mem_alloc_func fpdec_mem_alloc UNUSED = calloc;
static mem_free_func fpdec_mem_free UNUSED = free;

#endif //FPDEC_MEM_H
