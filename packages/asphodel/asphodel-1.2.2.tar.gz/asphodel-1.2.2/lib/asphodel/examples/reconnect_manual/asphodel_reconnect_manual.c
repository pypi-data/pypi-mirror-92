/*
 * Copyright (c) 2017, Suprock Technologies
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
 * SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
 * OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include <time.h>

#if defined(_MSC_VER) && _MSC_VER < 1900 // NOTE: 1900 is VS2015
	#include "inttypes.h"
#else
	#include <inttypes.h>
#endif

#include "snprintf.h" // for msvc++ compatability

#include "asphodel.h"

#ifdef _WIN32
	#include <conio.h>
#else
	#define _getch getchar
	#include <termios.h>
	#include <unistd.h>
	#include <fcntl.h>

	int _kbhit(void)
	{
		struct termios oldt, newt;
		int ch;
		int oldf;

		tcgetattr(STDIN_FILENO, &oldt);
		newt = oldt;
		newt.c_lflag &= ~(ICANON | ECHO);
		tcsetattr(STDIN_FILENO, TCSANOW, &newt);
		oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
		fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

		ch = getchar();

		tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
		fcntl(STDIN_FILENO, F_SETFL, oldf);

		if(ch != EOF)
		{
			ungetc(ch, stdin);
			return 1;
		}

		return 0;
	}

#endif


typedef struct {
	AsphodelDeviceDecoder_t *decoder;
	int stream_count;
	AsphodelStreamAndChannels_t *info_array;
	char serial_number[100];
} DeviceInfo_t;

static void lost_packet_callback(uint64_t current, uint64_t last, void * closure)
{
	char *info_str = (char*)closure;
	uint64_t lost = (current - last) - 1;

	fprintf(stderr, "Lost %" PRIu64 " packets on %s\n", lost, info_str);
}

static void unknown_id_callback(uint8_t id, void * closure)
{
	DeviceInfo_t *device_info = (DeviceInfo_t*)closure;
	fprintf(stderr, "Unknown stream id %d on %s\n", id, device_info->serial_number);
}

static int create_device_info(AsphodelDevice_t *device, DeviceInfo_t **device_info)
{
	int ret;
	int count;
	int i;
	uint8_t filler_bits;
	uint8_t id_bits;
	AsphodelDeviceDecoder_t *decoder;
	AsphodelStreamAndChannels_t *info_array;
	DeviceInfo_t *allocated_device_info;

	allocated_device_info = (DeviceInfo_t*)malloc(sizeof(DeviceInfo_t));
	if (allocated_device_info == NULL)
	{
		printf("Out of memory!\n");
		return 1;
	}

	ret = device->get_serial_number(device, allocated_device_info->serial_number, sizeof(allocated_device_info->serial_number));
	if (ret != 0)
	{
		printf("Error %d in device->get_serial_number()\n", ret);
		free(allocated_device_info);
		return ret;
	}

	ret = asphodel_get_stream_count_blocking(device, &count, &filler_bits, &id_bits);
	if (ret != 0)
	{
		printf("Error %d in asphodel_get_stream_count_blocking()\n", ret);
		free(allocated_device_info);
		return ret;
	}

	if (count == 0)
	{
		// no streams
		allocated_device_info->decoder = NULL;
		allocated_device_info->info_array = NULL;
		allocated_device_info->stream_count = 0;
		*device_info = allocated_device_info;
		return 0;
	}

	info_array = (AsphodelStreamAndChannels_t*)malloc(sizeof(AsphodelStreamAndChannels_t) * count);
	if (info_array == NULL)
	{
		printf("Out of memory!\n");
		free(allocated_device_info);
		return 1;
	}

	for (i = 0; i < count; i++)
	{
		int j;

		info_array[i].stream_id = i;

		ret = asphodel_get_stream_blocking(device, i, &info_array[i].stream_info);
		if (ret != 0)
		{
			int m;

			printf("Error %d in asphodel_get_stream_blocking(%d)\n", ret, i);

			// free the partially filled info array
			for (m = 0; m < i; m++)
			{
				int n;
				for (n = 0; n < info_array[m].stream_info->channel_count; n++)
				{
					asphodel_free_channel(info_array[m].channel_info[n]);
				}
				free(info_array[m].channel_info);
				asphodel_free_stream(info_array[m].stream_info);
			}
			free(info_array);

			free(allocated_device_info);

			return ret;
		}

		if (info_array[i].stream_info->channel_count == 0)
		{
			int m;

			printf("Error: stream %d has 0 channels!\n", i);

			asphodel_free_stream(info_array[i].stream_info);

			// free the partially filled info array
			for (m = 0; m < i; m++)
			{
				int n;
				for (n = 0; n < info_array[m].stream_info->channel_count; n++)
				{
					asphodel_free_channel(info_array[m].channel_info[n]);
				}
				free(info_array[m].channel_info);
				asphodel_free_stream(info_array[m].stream_info);
			}
			free(info_array);

			free(allocated_device_info);

			return 1;
		}

		info_array[i].channel_info = (AsphodelChannelInfo_t**)malloc(sizeof(AsphodelChannelInfo_t*) * info_array[i].stream_info->channel_count);
		if (info_array[i].channel_info == NULL)
		{
			int m;

			printf("Out of memory!\n");

			asphodel_free_stream(info_array[i].stream_info);

			// free the partially filled info array
			for (m = 0; m < i; m++)
			{
				int n;
				for (n = 0; n < info_array[m].stream_info->channel_count; n++)
				{
					asphodel_free_channel(info_array[m].channel_info[n]);
				}
				free(info_array[m].channel_info);
				asphodel_free_stream(info_array[m].stream_info);
			}
			free(info_array);

			free(allocated_device_info);

			return 1;
		}

		for (j = 0; j < info_array[i].stream_info->channel_count; j++)
		{
			uint8_t channel_index = info_array[i].stream_info->channel_index_list[j];
			ret = asphodel_get_channel_blocking(device, channel_index, &info_array[i].channel_info[j]);
			if (ret != 0)
			{
				int m;

				printf("Error %d in asphodel_get_channel_blocking(%d)\n", ret, j);

				// free partially filled channel array
				for (m = 0; m < j; m++)
				{
					asphodel_free_channel(info_array[i].channel_info[m]);
				}
				free(info_array[i].channel_info);

				asphodel_free_stream(info_array[i].stream_info);

				// free the partially filled info array
				for (m = 0; m < i; m++)
				{
					int n;
					for (n = 0; n < info_array[m].stream_info->channel_count; n++)
					{
						asphodel_free_channel(info_array[m].channel_info[n]);
					}
					free(info_array[m].channel_info);
					asphodel_free_stream(info_array[m].stream_info);
				}
				free(info_array);

				free(allocated_device_info);

				return ret;
			}
		}
	}

	ret = asphodel_create_device_decoder(info_array, count, filler_bits, id_bits, &decoder);
	if (ret != 0)
	{
		printf("Error %d in asphodel_create_device_decoder(%d)\n", ret, i);

		// free info_array
		for (i = 0; i < count; i++)
		{
			int j;
			for (j = 0; j < info_array[i].stream_info->channel_count; j++)
			{
				asphodel_free_channel(info_array[i].channel_info[j]);
			}
			free(info_array[i].channel_info);
			asphodel_free_stream(info_array[i].stream_info);
		}
		free(info_array);

		free(allocated_device_info);

		return ret;
	}

	allocated_device_info->decoder = decoder;
	allocated_device_info->stream_count = count;
	allocated_device_info->info_array = info_array;

	decoder->unknown_id_callback = unknown_id_callback;
	decoder->unknown_id_closure = allocated_device_info;

	for (i = 0; i < (int)decoder->streams; i++)
	{
		AsphodelStreamDecoder_t *stream_decoder = decoder->decoders[i];
		char *info_str;

		info_str = (char*)malloc(256);
		if (info_str == NULL)
		{
			printf("Out of memory!\n");
			// NOTE: returning without freeing things; this will leak memory
			return 1;
		}
		snprintf(info_str, 256, "%s stream %d", allocated_device_info->serial_number, i);

		stream_decoder->lost_packet_callback = lost_packet_callback;
		stream_decoder->lost_packet_closure = info_str;
	}

	*device_info = allocated_device_info;
	return 0;
}

static void free_device_info(DeviceInfo_t *device_info)
{
	size_t i;

	for (i = 0; i < device_info->decoder->streams; i++)
	{
		AsphodelStreamDecoder_t *stream_decoder = device_info->decoder->decoders[i];

		free(stream_decoder->lost_packet_closure);
	}

	device_info->decoder->free_decoder(device_info->decoder);

	for (i = 0; i < (size_t)device_info->stream_count; i++)
	{
		int j;

		for (j = 0; j < device_info->info_array[i].stream_info->channel_count; j++)
		{
			asphodel_free_channel(device_info->info_array[i].channel_info[j]);
		}

		free(device_info->info_array[i].channel_info);
		asphodel_free_stream(device_info->info_array[i].stream_info);
	}

	free(device_info->info_array);
	free(device_info);
}

static void streaming_packet_callback(int status, const uint8_t *stream_data, size_t packet_size, size_t packet_count, void * closure)
{
	if (status == 0)
	{
		size_t i;
		DeviceInfo_t *device_info = (DeviceInfo_t*)closure;
		for (i = 0; i < packet_count; i++)
		{
			const uint8_t *buffer = &stream_data[i * packet_size];
			device_info->decoder->decode(device_info->decoder, buffer);
		}
	}
	else
	{
		printf("Bad status %d in streaming_packet_callback()\n", status);
	}
}

int main(void)
{
	int ret;
	size_t list_size;
	size_t array_size;
	AsphodelDevice_t **device_array;
	DeviceInfo_t **device_info_array;
	size_t i;

	// initialize the library
	ret = asphodel_usb_init();
	if (ret != 0)
	{
		printf("Error %d in asphodel_usb_init()\n", ret);
		return ret;
	}

	while (1)
	{
		// get the number of devices available
		list_size = 0;
		ret = asphodel_usb_find_devices(NULL, &list_size);
		if (ret != 0)
		{
			printf("Error %d in 1st asphodel_usb_find_devices()\n", ret);
			return ret;
		}

		if (list_size == 0)
		{
			printf("No Devices Found! Press any key to rescan...\n");
			while (_kbhit() == 0)
			{
				asphodel_usb_poll_devices(100);
			}
			_getch(); // consume key
			continue;
		}

		array_size = list_size;
		device_array = (AsphodelDevice_t**)malloc(sizeof(AsphodelDevice_t *) * array_size);
		if (device_array == NULL)
		{
			printf("Out of Memory!\n");
			return 1;
		}

		device_info_array = (DeviceInfo_t**)malloc(sizeof(DeviceInfo_t*) * array_size);
		if (device_info_array == NULL)
		{
			printf("Out of Memory!\n");
			free(device_array);
			return 1;
		}

		ret = asphodel_usb_find_devices(device_array, &list_size);
		if (ret != 0)
		{
			printf("Error %d in 2nd asphodel_usb_find_devices()\n", ret);
			free(device_array);
			free(device_info_array);
			return ret;
		}

		// take the minimum of array_size and list_size
		array_size = (array_size < list_size) ? array_size : list_size;

		if (array_size == 1)
		{
			printf("Found %d device!\n", (int)array_size);
		}
		else
		{
			printf("Found %d devices!\n", (int)array_size);
		}

		for (i = 0; i < array_size; i++)
		{
			AsphodelDevice_t *device = device_array[i];

			ret = device->open_device(device);
			if (ret != 0)
			{
				size_t j;

				printf("Error %d in device->open_device()\n", ret);

				for (j = 0; j < i; j++)
				{
					device_array[j]->close_device(device_array[j]);
					free_device_info(device_info_array[j]);
					device_array[j]->free_device(device_array[j]);
				}
				free(device_array);
				free(device_info_array);

				return ret;
			}

			ret = create_device_info(device, &device_info_array[i]);
			if (ret != 0)
			{
				size_t j;

				// already printed error

				device->close_device(device);

				for (j = 0; j < i; j++)
				{
					device_array[j]->close_device(device_array[j]);
					free_device_info(device_info_array[j]);
					device_array[j]->free_device(device_array[j]);
				}
				free(device_array);
				free(device_info_array);

				return ret;
			}
		}

		for (i = 0; i < array_size; i++)
		{
			double response_time;
			double buffer_time;
			int packet_count;
			int transfer_count;
			unsigned int timeout;
			int j;
			AsphodelDevice_t *device = device_array[i];
			DeviceInfo_t *device_info = device_info_array[i];

			if (device_info->stream_count == 1)
			{
				printf("Enabling %d stream from %s\n", device_info->stream_count, device_info->serial_number);
			}
			else
			{
				printf("Enabling %d streams from %s\n", device_info->stream_count, device_info->serial_number);
			}

			response_time = 0.100; // 100 milliseconds
			buffer_time = 0.500; // 500 milliseconds
			timeout = 1000; // 1000 milliseconds

			ret = asphodel_get_streaming_counts(device_info->info_array, device_info->stream_count, response_time, buffer_time, &packet_count, &transfer_count, &timeout);
			if (ret != 0)
			{
				size_t k;

				printf("Error %d in asphodel_get_streaming_counts()\n", ret);

				for (k = 0; k < array_size; k++)
				{
					AsphodelDevice_t *device = device_array[k];
					DeviceInfo_t *device_info = device_info_array[k];

					if (k < i)
					{
						int m;
						for (m = 0; m < device_info->stream_count; m++)
						{
							// ignore any errors; we're already closing the device
							asphodel_enable_stream_blocking(device, device_info->info_array[m].stream_id, 0);
						}

						device->stop_streaming_packets(device);
						device->poll_device(device, 10, NULL); // call poll so the cancelled stream callbacks can complete before closing the device
					}
					device->close_device(device);
					free_device_info(device_info);
					device->free_device(device);
				}
				free(device_array);
				free(device_info_array);

				return ret;
			}

			printf("Transfer count: %d\n", transfer_count);

			device->start_streaming_packets(device, packet_count, transfer_count, timeout, streaming_packet_callback, device_info);

			for (j = 0; j < device_info->stream_count; j++)
			{
				ret = asphodel_enable_stream_blocking(device, device_info->info_array[j].stream_id, 1);
				if (ret != 0)
				{
					size_t k;

					printf("Error %d in asphodel_enable_stream_blocking()\n", ret);

					for (k = 0; k < (size_t)j; k++)
					{
						// ignore any errors; we're already closing the device
						asphodel_enable_stream_blocking(device, device_info->info_array[k].stream_id, 0);
					}

					device->stop_streaming_packets(device);
					device->poll_device(device, 10, NULL);  // call poll so the cancelled stream callbacks can complete before closing the device

					for (k = 0; k < array_size; k++)
					{
						AsphodelDevice_t *device = device_array[k];
						DeviceInfo_t *device_info = device_info_array[k];

						if (k < i)
						{
							int m;
							for (m = 0; m < device_info->stream_count; m++)
							{
								// ignore any errors; we're already closing the device
								asphodel_enable_stream_blocking(device, device_info->info_array[m].stream_id, 0);
							}

							device->stop_streaming_packets(device);
							device->poll_device(device, 10, NULL); // call poll so the cancelled stream callbacks can complete before closing the device
						}
						device->close_device(device);
						free_device_info(device_info);
						device->free_device(device);
					}
					free(device_array);
					free(device_info_array);

					return ret;
				}
			}
		}

		printf("Press any key to restart data collection...\n");
		while (_kbhit() == 0)
		{
			asphodel_usb_poll_devices(100);
		}
		_getch(); // consume key

		for (i = 0; i < array_size; i++)
		{
			int j;
			AsphodelDevice_t *device = device_array[i];
			DeviceInfo_t *device_info = device_info_array[i];

			if (device_info->stream_count == 1)
			{
				printf("Disabling %d stream from %s\n", device_info->stream_count, device_info->serial_number);
			}
			else
			{
				printf("Disabling %d streams from %s\n", device_info->stream_count, device_info->serial_number);
			}

			for (j = 0; j < device_info->stream_count; j++)
			{
				ret = asphodel_enable_stream_blocking(device, device_info->info_array[j].stream_id, 0);
				if (ret != 0)
				{
					printf("Error %d in asphodel_enable_stream_blocking()\n", ret);

					// might as well continue the cleanup process
					continue;
				}
			}
		}

		for (i = 0; i < array_size; i++)
		{
			AsphodelDevice_t *device = device_array[i];
			DeviceInfo_t *device_info = device_info_array[i];

			device->stop_streaming_packets(device);
			device->poll_device(device, 10, NULL); // call poll so the cancelled stream callbacks can complete before closing the device
			device->close_device(device);
			free_device_info(device_info);
			device->free_device(device);
		}

		free(device_array);
		free(device_info_array);
	}

	// close the library
	asphodel_usb_deinit();

	return 0;
}
