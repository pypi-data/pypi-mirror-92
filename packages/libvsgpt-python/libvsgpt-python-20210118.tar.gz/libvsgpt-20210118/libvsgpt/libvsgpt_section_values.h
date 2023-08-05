/*
 * The section values functions
 *
 * Copyright (C) 2019-2021, Joachim Metz <joachim.metz@gmail.com>
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

#if !defined( _LIBVSGPT_SECTION_VALUES_H )
#define _LIBVSGPT_SECTION_VALUES_H

#include <common.h>
#include <types.h>

#include "libvsgpt_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct libvsgpt_section_values libvsgpt_section_values_t;

struct libvsgpt_section_values
{
	/* The type
	 */
	uint8_t type;

	/* The offset
	 */
	off64_t offset;

	/* The size
	 */
	size64_t size;
};

int libvsgpt_section_values_initialize(
     libvsgpt_section_values_t **section_values,
     libcerror_error_t **error );

int libvsgpt_section_values_free(
     libvsgpt_section_values_t **section_values,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBVSGPT_SECTION_VALUES_H ) */

