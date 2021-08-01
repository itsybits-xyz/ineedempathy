import { FC, useState } from 'react';
import { PlaySound } from '.';
import { MdVolumeUp } from 'react-icons/md';
import { Container, Row } from 'react-bootstrap';

export const VolumeControl: FC = () => {
  const [ showOptions, setShowOptions ] = useState(false);
  const { volume, playToggle } = PlaySound();
  return (
    <Container id="volume-control">
      { showOptions && (
        <Row className="justify-content-sm-center">
          <PlaySound.VolumeEl
            {...volume}
            onChange={playToggle} />
        </Row>
      )}
      <Row className="justify-content-sm-center">
        <MdVolumeUp
          onClick={() => {
            setShowOptions(!showOptions);
          }}
          size={24} />
      </Row>
    </Container>
  );
};
