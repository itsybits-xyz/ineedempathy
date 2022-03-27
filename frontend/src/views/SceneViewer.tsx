import React, { FC, useState, useEffect } from 'react';
import { Scene, Story, Card } from '../schemas';
import { createGuess, getCards, getStory, getScene } from '../utils';
import { Row, Col, Container, Spinner } from 'react-bootstrap';
import { EmpathyResults } from './EmpathyResults';
import { EmpathyGuess } from './EmpathyGuess';
import { NavLink, Link } from 'react-router-dom';
import { RandomIcon } from './RandomIcon';
import './SceneViewer.scss';

export interface SceneProps {
  match: {
    params: {
      storyId: string
      position: string
    }
  }
}

export const SceneViewer: FC<SceneProps> = (props: SceneProps) => {
  const storyId: number = parseInt(props.match.params.storyId, 10)
  const position: number = parseInt(props.match.params.position, 10)
  const [ story, setStory ] = useState<Story>()
  const [ cards, setCards ] = useState<Card[]>([])
  const [ cardGuesses, setCardGuesses ] = useState<number[]>([])
  const [ madeGuess, setMadeGuess ] = useState<boolean>(false)
  const [ renderId, setRenderId ] = useState<number>(0)

  const isActiveForScene = (id:number) => {
    const navLinkMatch = new RegExp(`/scene/${id}$`)
    return (match:any, location:any) => {
      return location?.pathname?.match(navLinkMatch);
    };
  };

  useEffect(() => {
    setRenderId(Math.floor(Math.random() * 1000))
    setMadeGuess(false)
  }, [storyId, position]);

  useEffect(() => {
    getStory({storyId}).then((story: Story) => {
      setStory(story);
    })
    getCards().then((cards: Card[]) => {
      setCards(cards);
    });
  }, [storyId]);

  if (!story || !story.displayName || !story.scenes || story.scenes.length === 0) {
    return (
      <Spinner animation="border" variant="info">
        <span className="sr-only">Loading...</span>
      </Spinner>
    );
  }

  const scene: Scene = story.scenes.find((scene) => scene.position === position) || story.scenes[0]
  const hasNextScene = !!story.scenes.find((scene) => scene.position === position + 1)

  const handleSubmit = (cards: Card[]) => {
    const params = { storyId, sceneId: scene.id }
    setMadeGuess(true)
    return Promise.all(cards.map((card: Card) => {
      return createGuess(params, card)
    })).then(() => {
      return getScene(params).then((scene: Scene) => {
        setCardGuesses(scene.cardGuesses)
      });
    });
  }

  return (
    <>
      <div className="content scene-viewer">
        <Container fluid>
          <Row>
            <Col xs={12} md={4} lg={3} className="nav-bar">
              {story.scenes.map((scene, idx) => {
                return (
                  <NavLink
                    key={idx}
                    to={`/story/${storyId}/scene/${scene.position}`}
                    className="nav-link"
                    isActive={isActiveForScene(scene.position)}
                    activeClassName="active">
                    <RandomIcon string={scene.description} size={32} />
                    <p>
                      Scene {scene.position}
                    </p>
                  </NavLink>
                );
              })}
            </Col>
            <Col xs={12} md={8} lg={9}>
              <h2>{ story.displayName }</h2>
              <h3>Scene { position }</h3>
              <p className="scene-description">{ scene.description }</p>
            </Col>
          </Row>
          {madeGuess && (
            hasNextScene ? (
              <Row>
                <h3>
                  <span>You finished this scene, would you like to go to the&nbsp;</span>
                  <Link
                    title={`Next Scene`}
                    to={`/story/${storyId}/scene/${position+1}`}>
                    next scene
                  </Link>
                  <span>?</span>
                </h3>
              </Row>
            ) : (
              <Row>
                <h3>
                  <span>You finished this story, would you like to&nbsp;</span>
                  <Link
                    title={`Browse more stories`}
                    to={`/stories`}>
                    Browse more stories
                  </Link>
                  <span>?</span>
                </h3>
              </Row>
            )
          )}
          <hr />
          <Row>
            { madeGuess ? (
              <EmpathyResults
                cards={cards}
                cardGuesses={cardGuesses} />
            ) : (
              <EmpathyGuess
                rerender={renderId}
                cards={cards}
                noun={scene.noun}
                onSubmit={handleSubmit} />
            )}
          </Row>
        </Container>
      </div>
    </>
  );
};
