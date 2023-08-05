/*
 * The Master Boot Record (MBR) partition type functions
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

#if !defined( _LIBVSGPT_MBR_PARTITION_TYPE_H )
#define _LIBVSGPT_MBR_PARTITION_TYPE_H

#include <common.h>
#include <types.h>

#if defined( __cplusplus )
extern "C" {
#endif

#if defined( HAVE_DEBUG_OUTPUT )

typedef struct libvsgpt_mbr_partition_type libvsgpt_mbr_partition_type_t;

struct libvsgpt_mbr_partition_type
{
	/* The type
	 */
	uint16_t type;

	/* The description
	 */
	const char *description;
};

const char *libvsgpt_mbr_partition_type_get_description(
             uint8_t partition_type );

#endif /* defined( HAVE_DEBUG_OUTPUT ) */

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBVSGPT_MBR_PARTITION_TYPE_H ) */

