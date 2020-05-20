#coding=utf-8
import paramiko
import time
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig

if __name__ == '__main__':
    yamlconfig_obj = DataGetConfig()
    yamlConfig = yamlconfig_obj.getConfig('audio_recordAndPlay_command.yaml')
    print('yamlConfig: ', yamlConfig)
    host_ip = yamlConfig['Host_IP']
    print(host_ip)
    ssh_name = yamlConfig['SSH_Name']
    ssh_pwd = yamlConfig['SSH_Password']
    print(ssh_pwd)
    ssh_port = yamlConfig['SSH_Port']
    print(ssh_port)
    delay_time = 6

    Test_max = 2

    ss = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
    ss.connects()

    for i in range(1, Test_max+1):
        print("-----------------------------------Record start:  ", i, " Times-------------------------------\n")
        print(ss.send_data(yamlConfig.get('audio_record_pathway')))
        print(ss.send_data(yamlConfig.get('set_audio_record_volume')))
        print(ss.send_data(yamlConfig.get('audio_record_start')))
        print('请开始录音')
        time.sleep(delay_time)
        print(ss.send_data(yamlConfig.get('audio_record_stop')))
        print('录音结束')
        
        print("-----------------------------------Player start:  ", i, " Times-------------------------------\n")
    
        print(ss.send_data(yamlConfig.get('audio_play_pathway')))
        print(ss.send_data(yamlConfig.get('set_audio_player_volume')))
        print(ss.send_data(yamlConfig.get('auido_play_start')))
        print('开始播放音乐')
        time.sleep(delay_time)
        print(ss.send_data(yamlConfig.get('audio_play_stop')))
        print('播放结束')

    ss.disconnect()