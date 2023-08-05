/*
 * Support functions
 *
 * Copyright (C) 2012-2020, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _LIBCTHREADS_SUPPORT_H )
#define _LIBCTHREADS_SUPPORT_H

#include <common.h>
#include <types.h>

#include "libcthreads_extern.h"

#if defined( __cplusplus )
extern "C" {
#endif

#if !defined( HAVE_LOCAL_LIBCTHREADS )

LIBCTHREADS_EXTERN \
const char *libcthreads_get_version(
             void );

#endif /* !defined( HAVE_LOCAL_LIBCTHREADS ) */

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBCTHREADS_SUPPORT_H ) */

