#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x3868185, "module_layout" },
	{ 0x58aa99e6, "param_ops_int" },
	{ 0x4a78bd38, "single_release" },
	{ 0xdd706452, "seq_lseek" },
	{ 0xb3453dc4, "seq_read" },
	{ 0xd99a617, "remove_proc_entry" },
	{ 0xfe990052, "gpio_free" },
	{ 0xc6f182b9, "proc_create_data" },
	{ 0x403f9529, "gpio_request_one" },
	{ 0xc5850110, "printk" },
	{ 0x86332725, "__stack_chk_fail" },
	{ 0xec3d2e1b, "trace_hardirqs_off" },
	{ 0x848b4a19, "seq_printf" },
	{ 0xd697e69a, "trace_hardirqs_on" },
	{ 0xc4f0da12, "ktime_get_with_offset" },
	{ 0xe3e779ad, "gpiod_direction_input" },
	{ 0x6362cb11, "gpiod_set_raw_value" },
	{ 0x84f696ed, "gpiod_direction_output_raw" },
	{ 0x8e865d3c, "arm_delay_ops" },
	{ 0x8f678b07, "__stack_chk_guard" },
	{ 0x2db72154, "gpiod_get_raw_value" },
	{ 0xc5e1beab, "gpio_to_desc" },
	{ 0xf9a482f9, "msleep" },
	{ 0x20f76309, "single_open" },
	{ 0x37befc70, "jiffies_to_msecs" },
	{ 0x526c3a6c, "jiffies" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "AC134FD33A7244E4C1F3F00");
