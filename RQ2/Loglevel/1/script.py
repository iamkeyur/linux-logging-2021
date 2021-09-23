import os
import re
with open('newdata.csv', 'r') as f:
    ll = f.readlines()

verb = re.compile(
        "KERN_EMERG|KERN_ALERT|KERN_CRIT|KERN_ERR|KERN_WARNING|KERN_NOTICE|KERN_INFO|KERN_DEBUG|KERN_CONT")

def get_printk_level(content):
    level = 99  # which is default
    if "KERN_EMERG" in content or "UM_KERN_EMERG" in content:
        level = 0
    elif "KERN_ALERT" in content or "UM_KERN_ALERT" in content:
        level = 1
    elif "KERN_CRIT" in content or "UM_KERN_CRIT" in content:
        level = 2
    elif "KERN_ERR" in content or "UM_KERN_ERR" in content or "MYIOC_s_ERR_FMT" in content:
        level = 3
    elif "KERN_WARNING" in content or "UM_KERN_WARNING" in content or "MYIOC_s_WARN_FMT" in content:
        level = 4
    elif "KERN_NOTICE" in content or "UM_KERN_NOTICE" in content or "OSST_DEB_MSG" in content or "MYIOC_s_NOTE_FMT" in content:
        level = 5
    elif "KERN_INFO" in content or "UM_KERN_INFO" in content or "MYIOC_s_INFO_FMT" in content:
        level = 6
    elif "KERN_DEBUG" in content or "UM_KERN_DEBUG" in content or "MYIOC_s_DEBUG_FMT" in content or "RTAS_DEBUG" in content or "JFFS2_DBG" in content:
        level = 7
    elif "KERN_DEFAULT" in content:
        level = 99
    elif "KERN_CONT" in content or "UM_KERN_CONT" in content:
        level = 8

    return level


def get_level(content):
    level = "UNKNOWN"
    if "emerg" in content or "panic" in content:
        level = 0
    elif "alert" in content or "um_kern_alert" in content:
        level = 1
    elif "crit" in content or "um_kern_crit" in content:
        level = 2
    elif "err" in content or "pr_vlog" in content or "print_er" in content or "xenbus_dev_fatal" in content:
        level = 3
    elif "warn" in content or "um_kern_warning" in content or "myioc_s_warn_fmt" in content:
        level = 4
    elif "notice" in content or "um_kern_notice" in content or "osst_deb_msg" in content or "myioc_s_note_fmt" in content:
        level = 5
    elif "info" in content or "um_kern_info" in content or "myioc_s_info_fmt" in content:
        level = 6
    elif "debug" in content or "dbg" in content or "dm_output_to_console" in content or "rt_trace" in content or "btc_alg_dbg" in content or 'qeth_dbf_text_' in content or 'qeth_card_text_' in content or 'print_d' in content or 'zcrypt_dbf' in content:
        level = 7
    elif "cont" in content:
        level = 8

    return level

all_printk = ['printk', 'dev_printk', 'edac_printk', 'netdev_printk',
               'pci_printk', 'printk_in_rcu', 'printk_once', 'printk_ratelimited',
               'scmd_printk', 'sdev_printk', 'shost_printk', 'ssb_printk', 'ecryptfs_printk', 
               'netdev_printk', 'netif_printk', 'printk_deferred', 'printk_deferred_once', 
               'printk_ratelimited', 'nilfs_msg', 'dsprintk', 'dprintk', 'ir_dprintk',
                'vdbg_printk', 'arc_printk', 'dbg_printk', 'dprintk0', 'err_printk', 'sas_printk', 'warn_printk',
                'dprintk_cont', 'btc_print','btc_alg_dbg','btc_iface_dbg', 'printk_ratelimited_in_rcu']

printk_like = ['printk', 'dev_printk', 'edac_printk', 'netdev_printk',
               'pci_printk', 'printk_in_rcu', 'printk_once', 'printk_ratelimited',
               'scmd_printk', 'sdev_printk', 'shost_printk', 'ssb_printk', 'ecryptfs_printk', 
               'netdev_printk', 'netif_printk', 'printk_deferred', 'printk_deferred_once', 
               'printk_ratelimited', 'nilfs_msg', 'printk_ratelimited_in_rcu']

debug_printk = ['dsprintk', 'dprintk', 'ir_dprintk',
                'vdbg_printk', 'arc_printk', 'dbg_printk', 'dprintk0',
                'btc_print', 'btc_alg_dbg','btc_iface_dbg']

err_printk = ['err_printk']

notice_printk = ['sas_printk']

warn_printk = ['warn_printk']

cont_printk = ['dprintk_cont']

printf = ['fprintf', 'seq_printf', 'ksft_print_msg', 'FAIL_PROP', 'drm_printf', 'ksft_exit_fail_msg']

for l in ll:
    dat = l.split("|||||")
    old_content = str(dat[2])
    new_content = str(dat[3]).rstrip()
    old = str(dat[0]).lower()
    new = str(dat[1]).lower()

    old_match = re.search(verb, old_content)
    new_match = re.search(verb, new_content)
    if old_match and new_match:
        old_level = get_printk_level(old_content)
        new_level = get_printk_level(new_content)
        print(str(old_level) + "->" + str(new_level))
        continue



# python script.py > out
# sort out | uniq -c > freq
# replace 99 with 4 => out2
# sort out2 | uniq -c > freq2
# grep -v "UNK" freq2 > final