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
            Learn to make an <strong>Empathy Guess</strong> by reading some
            short stories and seeing how others responded.
          </p>
          <p>
            An <strong>Empathy Guess</strong> usually consists of 1 feeling
            and 1 need in the form of a question. This is often a question
            because <strong>only</strong> the being experiencing the situation
            can tell you how they feel or what they need. We often only use one
            or two cards in an <strong>Empathy Guess</strong> so that we don't
            confuse or overwhelm others.
          </p>
          <p>
            Click a story below to get started.
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
