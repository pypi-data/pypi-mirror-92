/*
 * ISO 8859-16 codepage (Latin 10) function
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

#include <common.h>
#include <types.h>

#include "libuna_codepage_iso_8859_16.h"

/* Extended ASCII to Unicode character lookup table for ISO 8859-16 codepage
 * Unknown are filled with the Unicode replacement character 0xfffd
 */
const uint16_t libuna_codepage_iso_8859_16_byte_stream_to_unicode_base_0xa0[ 96 ] = {
	0x00a0, 0x0104, 0x0105, 0x0141, 0x20ac, 0x201e, 0x0160, 0x00a7,
	0x0161, 0x00a9, 0x0218, 0x00ab, 0x0179, 0x00ad, 0x017a, 0x017b,
	0x00b0, 0x00b1, 0x010c, 0x0142, 0x017d, 0x201d, 0x00b6, 0x00b7,
	0x017e, 0x010d, 0x0219, 0x00bb, 0x0152, 0x0153, 0x0178, 0x017c,
	0x00c0, 0x00c1, 0x00c2, 0x0102, 0x00c4, 0x0106, 0x00c6, 0x00c7,
	0x00c8, 0x00c9, 0x00ca, 0x00cb, 0x00cc, 0x00cd, 0x00ce, 0x00cf,
	0x0110, 0x0143, 0x00d2, 0x00d3, 0x00d4, 0x0150, 0x00d6, 0x015a,
	0x0170, 0x00d9, 0x00da, 0x00db, 0x00dc, 0x0118, 0x021a, 0x00df,
	0x00e0, 0x00e1, 0x00e2, 0x0103, 0x00e4, 0x0107, 0x00e6, 0x00e7,
	0x00e8, 0x00e9, 0x00ea, 0x00eb, 0x00ec, 0x00ed, 0x00ee, 0x00ef,
	0x0111, 0x0144, 0x00f2, 0x00f3, 0x00f4, 0x0151, 0x00f6, 0x015b,
	0x0171, 0x00f9, 0x00fa, 0x00fb, 0x00fc, 0x0119, 0x021b, 0x00ff
};

/* Unicode to ASCII character lookup table for ISO 8859-16 codepage
 * Unknown are filled with the ASCII replacement character 0x1a
 */
const uint8_t libuna_codepage_iso_8859_16_unicode_to_byte_stream_base_0x00a8[ 96 ] = {
	0x1a, 0xa9, 0x1a, 0xab, 0x1a, 0xad, 0x1a, 0x1a,
	0xb0, 0xb1, 0x1a, 0x1a, 0x1a, 0x1a, 0xb6, 0xb7,
	0x1a, 0x1a, 0x1a, 0xbb, 0x1a, 0x1a, 0x1a, 0x1a,
	0xc0, 0xc1, 0xc2, 0x1a, 0xc4, 0x1a, 0xc6, 0xc7,
	0xc8, 0xc9, 0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf,
	0x1a, 0x1a, 0xd2, 0xd3, 0xd4, 0x1a, 0xd6, 0x1a,
	0x1a, 0xd9, 0xda, 0xdb, 0xdc, 0x1a, 0x1a, 0xdf,
	0xe0, 0xe1, 0xe2, 0x1a, 0xe4, 0x1a, 0xe6, 0xe7,
	0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef,
	0x1a, 0x1a, 0xf2, 0xf3, 0xf4, 0x1a, 0xf6, 0x1a,
	0x1a, 0xf9, 0xfa, 0xfb, 0xfc, 0x1a, 0x1a, 0xff,
	0x1a, 0x1a, 0xc3, 0xe3, 0xa1, 0xa2, 0xc5, 0xe5
};

const uint8_t libuna_codepage_iso_8859_16_unicode_to_byte_stream_base_0x0140[ 8 ] = {
	0x1a, 0xa3, 0xb3, 0xd1, 0xf1, 0x1a, 0x1a, 0x1a
};

const uint8_t libuna_codepage_iso_8859_16_unicode_to_byte_stream_base_0x0150[ 8 ] = {
	0xd5, 0xf5, 0xbc, 0xbd, 0x1a, 0x1a, 0x1a, 0x1a
};

const uint8_t libuna_codepage_iso_8859_16_unicode_to_byte_stream_base_0x0178[ 8 ] = {
	0xbe, 0xac, 0xae, 0xaf, 0xbf, 0xb4, 0xb8, 0x1a
};

const uint8_t libuna_codepage_iso_8859_16_unicode_to_byte_stream_base_0x0218[ 8 ] = {
	0xaa, 0xba, 0xde, 0xfe, 0x1a, 0x1a, 0x1a, 0x1a
};

