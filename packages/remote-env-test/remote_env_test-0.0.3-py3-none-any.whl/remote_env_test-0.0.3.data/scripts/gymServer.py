from concurrent import futures
import argparse
import grpc
from remote_env.env_pb2 import Info, Observation, Transition, Action
from remote_env.env_pb2_grpc import EnvServicer as Service, add_EnvServicer_to_server as register
print("gymServer started...")
# get installed package starting with gym prefix
import pkg_resources

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                  for i in installed_packages
                                  if (i.key.startswith('gym') or i.key.endswith('gym'))])
print("Available gym packages: ", installed_packages_list)

# gym packages to import
import gym

modules = sorted(["%s" % i.key.replace('-', '_')
                  for i in installed_packages
                  if ((i.key.startswith('gym') or i.key.endswith('gym')) and (i.key != 'gym'))])
for library in modules:
    try:
        exec("import {module}".format(module=library))
    except Exception as e:
        print(e)


def encode_observation(observation):
    return Observation(data=observation.ravel(), shape=observation.shape)


class Env(Service):

    def Make(self, name, _):
        name = name.value
        if not hasattr(self, 'env') or self.env.spec.id != name:
            self.env = gym.make(name)
        print('env {} created'.format(name))
        try:
            if self.env.observation_space.__class__ == gym.spaces.box.Box:
                observation_space_type = 'box'
            elif self.env.observation_space.__class__ == gym.spaces.Discrete:
                observation_space_type = 'discrete'
        except:
            observation_space_type = 'none'

        return Info(observation_space_type=observation_space_type,
                    observation_shape=self.env.observation_space.shape,
                    num_actions=self.env.action_space.n,
                    max_episode_steps=self.env._max_episode_steps)

    def Reset(self, empty, _):
        return encode_observation(self.env.reset())

    def Step(self, action, _):
        next_observation, reward, done, _ = self.env.step(action.value)
        next_observation = encode_observation(next_observation)
        return Transition(next_observation=next_observation,
                          reward=reward,
                          done=done)

    def Sample(self, empty, _):
        action = self.env.action_space.sample()
        return Action(value=action)

    def Close(self, empty, _):
        self.env.close()

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
class register_server():
    def Start(self,port):
        host = get_ip()
        address = '{}:{}'.format(host,port)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        register(Env(), server)
        server.add_insecure_port(address)
        server.start()
        print("started server at: {}".format(address))
        server.wait_for_termination()
        return 0

rs = register_server()
def Start(port):
    rs.Start(port)
    return 0
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser('environment server')
    parser.add_argument('--n', type = int)
    print("n=:",n)
    parser.add_argument('--host', type=str)
    #host = get_ip()
    #print('host=', host)
    parser.add_argument('--port', type=str)
    args = parser.parse_args()

    address = '{}:{}'.format(host,port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    register(Env(), server)
    server.add_insecure_port(address)
    server.start()
    print("started server at: {}".format(address))
    server.wait_for_termination()
    # try:
    #     while True:
    #         sleep(86400)
    # except KeyboardInterrupt:
    #     server.stop(0)
