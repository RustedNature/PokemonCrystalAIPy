import numpy as np
from Code.Enums.MapBank import MapBank
from Code.Enums.NeuborkiaMapNumber import NeuborkiaMapNumber
from Code.MemoryAddresses import MemoryAddresses


class RewardManager:
    def __init__(self):
        self.default_reward = 10.0
        self.max_pokemon_level = 100
        self.current_memory_values = None
        #self.last_images = []

        self.last_level_of_pokemon1 = 0
        self.current_level_of_pokemon1 = 0
        self.hp_of_pokemon1_byte1 = 0
        self.hp_of_pokemon1_byte2 = 0
        self.hp_of_pokemon1 = 0

        self.last_level_of_pokemon2 = 0
        self.current_level_of_pokemon2 = 0
        self.hp_of_pokemon2_byte1 = 0
        self.hp_of_pokemon2_byte2 = 0
        self.hp_of_pokemon2 = 0

        self.last_level_of_pokemon3 = 0
        self.current_level_of_pokemon3 = 0
        self.hp_of_pokemon3_byte1 = 0
        self.hp_of_pokemon3_byte2 = 0
        self.hp_of_pokemon3 = 0

        self.last_level_of_pokemon4 = 0
        self.current_level_of_pokemon4 = 0
        self.hp_of_pokemon4_byte1 = 0
        self.hp_of_pokemon4_byte2 = 0
        self.hp_of_pokemon4 = 0

        self.last_level_of_pokemon5 = 0
        self.current_level_of_pokemon5 = 0
        self.hp_of_pokemon5_byte1 = 0
        self.hp_of_pokemon5_byte2 = 0
        self.hp_of_pokemon5 = 0

        self.last_level_of_pokemon6 = 0
        self.current_level_of_pokemon6 = 0
        self.hp_of_pokemon6_byte1 = 0
        self.hp_of_pokemon6_byte2 = 0
        self.hp_of_pokemon6 = 0

        self.number_of_pokemon_in_team = 0

        self.last_map_bank = 0
        self.last_map_number = 0
        self.current_map_bank = 0
        self.current_map_number = 0

        self.world_y = 0
        self.last_world_y = 0
        self.world_x = 0
        self.last_world_x = 0
        self.same_spot_counter = 0

        self.battle_type = 0

        self.minutes_play_time_in_game = 0
        self.hours_play_time_in_game_byte1 = 0
        self.hours_play_time_in_game_byte2 = 0
        self.hours_play_time_in_game = 0

        self.got_oak_reward = False
        self.got_mom_reward = False
        self.got_outside_reward = False
        self.got_route_29_reward = False


        self.screen_in_hex = None
        self.last_tile_maps = []

        self.last_button_pressed = 0

    def route_29_reward(self):
        if self.current_map_bank == MapBank.Neuborkia.value and self.current_map_number == NeuborkiaMapNumber.Route29.value and not self.got_route_29_reward:
            self.reward += 10.0
            self.got_route_29_reward = True
            print("Reward for Route 29")

    def outside_reward(self):
        if self.current_map_bank == MapBank.Neuborkia.value and self.current_map_number == NeuborkiaMapNumber.Outside.value and not self.got_outside_reward:
            self.reward += 10.0
            self.got_outside_reward = True
            print("Reward for outside")

    def oak_lab_reward(self):
        if self.current_map_bank == MapBank.Neuborkia.value and self.current_map_number == NeuborkiaMapNumber.ProfHouse.value and not self.got_oak_reward:
            self.reward += 10.0
            self.got_oak_reward = True
            print("Reward for Oak lab")
    def mom_reward(self):
        if self.current_map_bank == MapBank.Neuborkia.value and self.current_map_number == NeuborkiaMapNumber.LivingRoom.value and (self.world_x == 8 or self.world_x == 9) and self.world_y == 4 and not self.got_mom_reward:
            self.reward += 10.0
            self.got_mom_reward = True
            print("Reward for Mom")

    def get_reward(self, last_button_pressed, image : np.ndarray, screen_in_hex):
        self.reward = 0.0
        #self.current_image = image.copy()
        self.last_button_pressed = last_button_pressed
        self.screen_in_hex = np.array(screen_in_hex)
        self.get_poitive_reward()
        #self.get_penalty()

        return self.reward
    
    import numpy as np

    def explo_rew(self):
        if len(self.last_tile_maps) == 0:
            self.last_tile_maps.append(self.screen_in_hex)
            return
        threshold = 0.1 * self.screen_in_hex.size
        # Compute the number of different tiles between the current tilemap and each previous tilemap
        differences = [np.sum(self.screen_in_hex != past_map) for past_map in self.last_tile_maps]

        # Check if all of the differences exceed the threshold
        are_all_above_threshold = all(difference > threshold for difference in differences)

        if are_all_above_threshold:
            self.reward += 0.01
            print("Reward for exploration")
            self.last_tile_maps.append(self.screen_in_hex)
    
    def get_poitive_reward(self):
        self.pokemon_level_reward()
        #self.exploration_reward()
        self.oak_lab_reward()
        self.mom_reward()
        self.outside_reward()
        self.route_29_reward()
        self.explo_rew()

    # def exploration_reward(self):
    #     if len(self.last_images) == 0:
    #         self.last_images.append(self.current_image)
    #         return
        
    #     is_different_image = self.is_image_different()
        
    #     if  is_different_image:
    #         self.last_images.append(self.current_image)
    #         self.reward += 0.01
    #         print("Reward for exploration")
            
 
    
    # def is_image_different(self):
    #     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    #     new_image_tensor = F.to_tensor(self.current_image.transpose((1, 2, 0))).to(device)
    #     new_image_norm = F.normalize(new_image_tensor, [0.5], [0.5])

    #     # Convert all images in self.last_images to tensors and stack them into a batch
    #     image_batch = torch.stack([F.to_tensor(img.transpose((1, 2, 0))).to(device) for img in self.last_images])

    #     # Normalize the batch of images
    #     image_batch_norm = F.normalize(image_batch, [0.5], [0.5])

    #     # Compute the absolute difference between the new image and each image in the batch
    #     diff = torch.abs_(new_image_norm - image_batch_norm)

    #     # Compute the mean difference for each image in the batch
    #     mean_diff = torch.mean(diff, dim=[1, 2])

    #     # Check if any of the mean differences are less than 0.2
    #     is_different = not torch.any(mean_diff < 0.000001)

    #     return is_different

    def pokemon_level_reward(self):
        if self.current_level_of_pokemon1 > self.last_level_of_pokemon1 and self.current_level_of_pokemon1 < self.max_pokemon_level and self.number_of_pokemon_in_team == 1:
            if self.last_level_of_pokemon1 == 0:
                self.reward += 10.0
                print("Reward for pokemon 1 catch")
            else:
                self.reward += 0.5
                print("Reward for pokemon 1 level up")
            self.last_level_of_pokemon1 = self.current_level_of_pokemon1
        elif self.current_level_of_pokemon2 > self.last_level_of_pokemon2 and self.current_level_of_pokemon2 < self.max_pokemon_level and self.number_of_pokemon_in_team == 2:
            if self.last_level_of_pokemon2 == 0:
                self.reward += 10.0
                print("Reward for pokemon 2 catch")
            else:
                self.reward += 0.5
                print("Reward for pokemon 2 level up")
            self.last_level_of_pokemon2 = self.current_level_of_pokemon2
        elif self.current_level_of_pokemon3 > self.last_level_of_pokemon3 and self.current_level_of_pokemon3 < self.max_pokemon_level and self.number_of_pokemon_in_team == 3:
            if self.last_level_of_pokemon3 == 0:
                self.reward += 10.0
                print("Reward for pokemon 3 catch")
            else:
                self.reward += 0.5
                print("Reward for pokemon 3 level up")
            self.last_level_of_pokemon3 = self.current_level_of_pokemon3
        elif self.current_level_of_pokemon4 > self.last_level_of_pokemon4 and self.current_level_of_pokemon4 < self.max_pokemon_level and self.number_of_pokemon_in_team == 4:
            if self.last_level_of_pokemon4 == 0:
                self.reward += 10.0
                print("Reward for pokemon 4 catch")
            else:
                self.reward += 0.5
                print("Reward for pokemon 4 level up")
            self.last_level_of_pokemon4 = self.current_level_of_pokemon4
        elif self.current_level_of_pokemon5 > self.last_level_of_pokemon5 and self.current_level_of_pokemon5 < self.max_pokemon_level and self.number_of_pokemon_in_team == 5:
            if self.last_level_of_pokemon5 == 0:
                self.reward += 10.0
                print("Reward for pokemon 5 catch")
            else:
                self.reward += 0.5
                print("Reward for pokemon 5 level up")
            self.last_level_of_pokemon5 = self.current_level_of_pokemon5
        elif self.current_level_of_pokemon6 > self.last_level_of_pokemon6 and self.current_level_of_pokemon6 < self.max_pokemon_level and self.number_of_pokemon_in_team == 6:
            if self.last_level_of_pokemon6 == 0:
                self.reward += 10.0
                print("Reward for pokemon 6 catch")
            else:
                self.reward += 0.5
                print("Reward for pokemon 6 level up")
            self.last_level_of_pokemon6 = self.current_level_of_pokemon6

    def get_penalty(self):
        if self.last_button_pressed == 6 or self.last_button_pressed == 7:
            self.reward -= 0.25
            #print("Penalty for pressing start or select")
    
    def reset(self):
        #self.last_images.clear()
        self.got_mom_reward = False
        self.got_oak_lab_reward = False
        self.got_outside_reward = False
        self.last_tile_maps.clear()

    def update_values(self, memory_value_list):
        for memval in memory_value_list:
            if memval.memAddress == MemoryAddresses.MapBank:
                self.current_map_bank = memval.memValue
            elif memval.memAddress == MemoryAddresses.MapNumber:
                self.current_map_number = memval.memValue
            elif memval.memAddress == MemoryAddresses.LevelOfPokemon1:
                self.current_level_of_pokemon1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon1Byte1:
                self.hp_of_pokemon1_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon1Byte2:
                self.hp_of_pokemon1_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.LevelOfPokemon2:
                self.current_level_of_pokemon2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon2Byte1:
                self.hp_of_pokemon2_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon2Byte2:
                self.hp_of_pokemon2_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.LevelOfPokemon3:
                self.current_level_of_pokemon3 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon3Byte1:
                self.hp_of_pokemon3_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon3Byte2:
                self.hp_of_pokemon3_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.LevelOfPokemon4:
                self.current_level_of_pokemon4 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon4Byte1:
                self.hp_of_pokemon4_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon4Byte2:
                self.hp_of_pokemon4_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.LevelOfPokemon5:
                self.current_level_of_pokemon5 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon5Byte1:
                self.hp_of_pokemon5_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon5Byte2:
                self.hp_of_pokemon5_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.LevelOfPokemon6:
                self.current_level_of_pokemon6 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon6Byte1:
                self.hp_of_pokemon6_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HpOfPokemon6Byte2:
                self.hp_of_pokemon6_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.NumberOfPokemonInTeam:
                self.number_of_pokemon_in_team = memval.memValue
            elif memval.memAddress == MemoryAddresses.BattleType:
                self.battle_type = memval.memValue
            elif memval.memAddress == MemoryAddresses.MinutesPlayTimeInGame:
                self.minutes_play_time_in_game = memval.memValue
            elif memval.memAddress == MemoryAddresses.HoursPlayTimeInGameByte1:
                self.hours_play_time_in_game_byte1 = memval.memValue
            elif memval.memAddress == MemoryAddresses.HoursPlayTimeInGameByte2:
                self.hours_play_time_in_game_byte2 = memval.memValue
            elif memval.memAddress == MemoryAddresses.WorldX:
                self.world_x = memval.memValue
            elif memval.memAddress == MemoryAddresses.WorldY:
                self.world_y = memval.memValue
