/*
 * UTF-8 stream functions
 *
 * Copyright (C) 2008-2020, Joachim Metz <joachim.metz@gmail.com>
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

#if !defined( _LIBUNA_UTF8_STREAM_H )
#define _LIBUNA_UTF8_STREAM_H

#include <common.h>
#include <types.h>

#include "libuna_extern.h"
#include "libuna_libcerror.h"
#include "libuna_types.h"

#if defined( __cplusplus )
extern "C" {
#endif

LIBUNA_EXTERN \
int libuna_utf8_stream_copy_byte_order_mark(
     uint8_t *utf8_stream,
     size_t utf8_stream_size,
     size_t *utf8_stream_index,
     libcerror_error_t **error );

LIBUNA_EXTERN \
int libuna_utf8_stream_size_from_utf8(
     const libuna_utf8_character_t *utf8_string,
     size_t utf8_string_size,
     size_t *utf8_stream_size,
     libcerror_error_t **error );

LIBUNA_EXTERN \
int libuna_utf8_stream_copy_from_utf8(
     uint8_t *utf8_stream,
     size_t utf8_stream_size,
     const libuna_utf8_character_t *utf8_string,
     size_t utf8_string_size,
     libcerror_error_t **error );

/* The functionality for libuna_utf8_stream_copy_to_utf8 is implemented by
 * libuna_utf8_string_copy_from_utf8_stream
 */

LIBUNA_EXTERN \
int libuna_utf8_stream_size_from_utf16(
     const libuna_utf16_character_t *utf16_string,
     size_t utf16_string_size,
     size_t *utf8_stream_size,
     libcerror_error_t **error );

LIBUNA_EXTERN \
int libuna_utf8_stream_copy_from_utf16(
     uint8_t *utf8_stream,
     size_t utf8_stream_size,
     const libuna_utf16_character_t *utf16_string,
     size_t utf16_string_size,
     libcerror_error_t **error );

/* The functionality for libuna_utf8_stream_copy_to_utf16 is implemented by
 * libuna_utf16_string_copy_from_utf8_stream
 */

LIBUNA_EXTERN \
int libuna_utf8_stream_size_from_utf32(
     const libuna_utf32_character_t *utf32_string,
     size_t utf32_string_size,
     size_t *utf8_stream_size,
     libcerror_error_t **error );

LIBUNA_EXTERN \
int libuna_utf8_stream_copy_from_utf32(
     uint8_t *utf8_stream,
     size_t utf8_stream_size,
     const libuna_utf32_character_t *utf32_string,
     size_t utf32_string_size,
     libcerror_error_t **error );

/* The functionality for libuna_utf8_stream_copy_to_utf32 is implemented by
 * libuna_utf32_string_copy_from_utf8_stream
 */

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBUNA_UTF8_STREAM_H ) */

