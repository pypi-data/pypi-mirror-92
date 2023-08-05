from concurrent import futures
import argparse
import gym
import grpc
from env_dict.SubProcDict import SubprocDictEnv

from grpc_env.envp_pb2 import Info, Observation, Observations, Transition, Transitions, \
    Actions, Empty, Renders, RenderOuts, RGBArry, EnvSeeds
from grpc_env.envp_pb2_grpc import EnvpServicer as Service, add_EnvpServicer_to_server as register


def encode_observation(observation):
    return Observation(data=observation.ravel(), shape=observation.shape)


def make_env(env_name):
    env = gym.make(env_name)
    return env


class Env(Service):
    env = SubprocDictEnv()

    def Make(self, name, _):
        name = name.data
        env_id = self.env.add_env(make_env, name)
        print('env {} with id {} created'.format(name, env_id))
        try:
            if self.env.observation_space[env_id].__class__ == gym.spaces.box.Box:
                observation_space_type = 'box'
            elif self.env.observation_space[env_id].__class__ == gym.spaces.Discrete:
                observation_space_type = 'discrete'
        except:
            observation_space_type = 'none'

        return Info(observation_space_type=observation_space_type,
                    observation_shape=self.env.observation_space[env_id].shape,
                    num_actions=self.env.action_space[env_id].n,
                    max_episode_steps=self.env._max_episode_steps[env_id],
                    env_id=env_id)

    def Reset(self, env_ids, _):
        obs = self.env.reset(env_ids.data)
        env_obs = [encode_observation(ob) for ob in obs]
        obs = Observations(obs=env_obs)
        return obs

    def Step(self, actions, _):

        next_observations, rewards, dones, _ = self.env.step(actions)
        transitions = []
        for i in range(len(next_observations)):
            next_obs = encode_observation(next_observations[i])
            transitions.append(Transition(next_observation=next_obs,
                                          reward=rewards[i],
                                          done=dones[i]))
        return Transitions(trans=transitions)

    def Sample(self, env_ids, _):
        # todo: test this function
        action = self.env.action_space.sample()
        return Actions(data=action)

    def Render(self, renders, _):
        res = self.env.render(renders)

        mode = renders.data
        if mode == 'rgb_array':
            reno = RenderOuts(rgb_array=[RGBArry(rgb=r.flatten()) for r in res])
        elif mode == 'ansi':
            reno = RenderOuts(ansi=res)
        elif mode == 'human':
            reno = RenderOuts()

        return reno

    def Seed(self, seeds, _):
        self.env.close(seeds)
        return Empty()

    def Close(self, env_ids, _):
        self.env.close(env_ids.data)
        return Empty()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('environment server')
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=str)

    args = parser.parse_args()

    address = '{}:{}'.format(args.host, args.port)

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
