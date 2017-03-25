'''
Author: Garyuu
Date:   2016/8/15
Name:   controller
Descr.: The core of the program. It's a bridge to most components.
'''
from library.socket_manager import SocketManager
import library.status as status
import threading

def __NULL_FUNCTION__():
    pass

class Controller:
    def __init__(self):
        # Prepare locks for racing condition
        self.process_lock =  threading.Lock()
        self.error_lock =  threading.Lock()
        self.error_timer = threading.Timer(3, __NULL_FUNCTION__)
        self.force_assign = False

        print("Initializing TCP server...")
        self.socket_manager = SocketManager(20000, 40, self.message_processor)
        self.socket_manager.start()
        
        print("Initializing status...")
        self.status = status.Status()
    
    #=================#
    # Message Process #
    #=================#
    def message_processor(self, message):
        if message['command'] == 'initialize':
            self.process_lock.acquire()
            if self.status.assign_machine_to_position(message['machine'], message['position'])
                resp_message = self.response_for_init(self.status.position_list[message['position']])
                self.process_lock.release()
            else:
                self.process_lock.release()
                self.error_lock.acquire()
                self.assign_error(message['machine'], message['position'], self.status.position_list[message['position'].machine_id])
                self.error_lock.release()
                if force_assign:
                    self.process_lock.acquire()
                    self.status.assign_machine_to_position(message['machine'], message['position'], True)
                    resp_message = self.response_for_init(self.status.position_list[message['position']])                    
                    self.process_lock.release()
                else:
                    resp_message = self.response(message['machine'], False)
        elif message['command'] == 'sendwave':
            self.process_lock.acquire()
            resp_message = self.response(message['machine'], self.status.save_wave_to_player(message))
            self.process_lock.release()
        else:
            resp_message = self.response(message['machine'], False)
        return resp_message

    def response(self, machine, status):
        resp = {
            'machine' : machine,
            'command' : 'response',
            'status'  : status,
        }
        return resp

    def response_for_init(self, position):
        resp = {
            'machine'     : machine,
            'command'     : 'setwave',
            'position'    : position.id,
            'wave'        : position.wave_count(),
            'shots'       : position.player_list[0].stage.shots_per_wave,
            'num_players' : len(position.player_list),
            'players'     : [],
            'scores'      : [],
        }
        for player in position.player_list:
            resp['players'].append(player.tag)
            resp['scores'].append(player.total_score())
        return resp

    def assign_error(self, machine, position, occupied_machine):
        color = "\x1b[2;37;42m"
        color_end = "\x1b[0m"
        print(color +
            "Machine {} cannot assigned to position {}, machine {} already occupied.\n".format(
                machine, position, occupied_machine) +
            "FORCE ASSIGN?(y/n) (Auto reject after 3 secs)" +
        color_end)
        self.force_assign = False
        self.error_timer.start()

    #==========#
    # Commands #
    #==========#
    def command_display_status(self):
        return str(self.status)

    def command_display_position(self, position):
        return str(self.status.position_list[position])

    def command_display_player(self, player_tag):
        return str(self.status.player_tag_dict[player_tag])

    def command_clear_status(self):
        self.status.clear()

    def command_assign_machine_to_position(self, machine, position):
        self.status.assign_machine_to_position(machine, position)

    def command_unlink_position(self, position):
        self.status.unlink_position(position)

    def command_error_decision(self, decision):
        if error_lock.acquire(False):
            error_lock.release()
        else:
            self.force_assign = decision
            self.error_timer.cancel()
