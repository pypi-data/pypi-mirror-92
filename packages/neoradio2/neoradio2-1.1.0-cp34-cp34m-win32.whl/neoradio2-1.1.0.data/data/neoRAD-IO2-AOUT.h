#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
	
typedef union _neoRADIO2AOUT_header {
	uint8_t byte;
	struct {
		unsigned ch1 :1;
		unsigned ch2 :1;
		unsigned ch3 :1;
		unsigned reserved :4;
		unsigned noCal:1;
	} bits;
} neoRADIO2AOUT_header;

typedef union _neoRADIO2AOUT_channelConfig{
	uint32_t u32;
	struct {
		uint16_t initOutputValue;
		uint8_t initEnabled;
		uint8_t enabled;
	} data;
} neoRADIO2AOUT_channelConfig;

#ifdef __cplusplus
}
#endif
