export interface Guess {
  cardId: number;
}

export interface CreateGuess {
  cardId: number;
  sceneId: number;
  storyId: number;
}

export interface SceneBase {
  id: number;
  storyId: number;
  noun: string;
  position: number;
  description: string;
  guesses: Guess[],
  cardGuesses: number[],
}

export interface Scene extends SceneBase {
}
