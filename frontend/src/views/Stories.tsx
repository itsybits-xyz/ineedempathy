import React, { FC, useState, useEffect } from 'react';
import { Story } from '../schemas';
import { getStories } from '../utils';
import { Row, Col, Container, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { ClickSound } from '../components';
import Identicon from 'react-identicons';

export const Stories: FC = () => {
  const [ stories, setStories ] = useState<Story[]>([]);

  useEffect(() => {
    getStories().then((data) => {
      setStories(data);
    })
  }, []);

  return (
    <div className="content fn-cards fn-stories">
      <Container fluid>
        <Row>
          <h2>Browse Stories</h2>
        </Row>
        <Row>
          <p>
            Learn to make an <strong>Empathy Guess</strong> by joining others
            and making guesses on short stories.
          </p>
        </Row>
        <Row>
          {stories.map((story) => {
            return (
              <Col>
                <Link
                  role="link"
                  title={`${story.displayName}`}
                  to={`/story/${story.id}/scene/1`}>
                  <ClickSound>
                    <Card>
                      <Card.Header>
                        <Identicon size={120} string={story.displayName} />
                      </Card.Header>
                      <Card.Body>
                        <Card.Title>{story.displayName}</Card.Title>
                      </Card.Body>
                    </Card>
                  </ClickSound>
                </Link>
              </Col>
            );
          })}
        </Row>
      </Container>
    </div>
  );
};
