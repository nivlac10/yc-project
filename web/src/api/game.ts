import { get, post } from "@/utils/http";

export class GameService {
    static get_game_play_url = (params?: object) => post('/get_game_play_url', params);
    static get_demo_game_play_url = (params?: object) => post('/get_demo_game_play_url', params);
}