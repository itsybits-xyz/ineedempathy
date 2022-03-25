import { Scene } from './scene';

export interface StoryBase {
  id: number;
  displayName: string;
  scenes ?: Scene[]
}

export interface Story extends StoryBase {
}
