#ifndef SNPRINTF_H_
#define SNPRINTF_H_

#include <stdio.h>
#include <stdarg.h>

// this code is based on http://stackoverflow.com/a/8712996/1011276

#if defined(_MSC_VER) && _MSC_VER < 1900 // NOTE: 1900 is VS2015

#define snprintf c99_snprintf
#define vsnprintf c99_vsnprintf

__inline int c99_vsnprintf(char *outBuf, size_t size, const char *format, va_list ap)
{
	int count = -1;

	if (size != 0)
		count = _vsnprintf_s(outBuf, size, _TRUNCATE, format, ap);
	if (count == -1)
		count = _vscprintf(format, ap);

	return count;
}

__inline int c99_snprintf(char *outBuf, size_t size, const char *format, ...)
{
	int count;
	va_list ap;

	va_start(ap, format);
	count = c99_vsnprintf(outBuf, size, format, ap);
	va_end(ap);

	return count;
}
#endif

#endif /* SNPRINTF_H_ */
