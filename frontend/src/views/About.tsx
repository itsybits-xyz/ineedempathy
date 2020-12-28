import React, { FC } from 'react';
import { Container } from 'react-bootstrap';
import { MdCloudCircle, MdAddAPhoto } from 'react-icons/md';

export const About: FC = () => {
  return (
    <>
      <div className="content">
        <Container fluid>
          <h2>About</h2>
          <p>
            This website is designed to create a guided gameplay to discover
            the empowerment that a “needs consciousness” gives you. Through
            play, this website aims to help create accessibility of this view
            of the world and empower you to not only give empathy to others,
            but more importantly to give empathy to yourself.
          </p>
        </Container>
        <Container fluid>
          <h2>Credits</h2>
          <ul>
            <li>
              Card Designs by&nbsp;
              <a href="https://www.instagram.com/susdraws/">
                Susana Castro
              </a>&nbsp;
              <a href="https://www.instagram.com/susdraws/">
                <MdAddAPhoto size={18}/>
              </a>&nbsp;
              <a href="http://susanacastro.net/">
                <MdCloudCircle size={18}/>
              </a>
            </li>
            <li>
              Material Dashboard Theme by&nbsp;
              <a href="https://www.creative-tim.com/product/material-dashboard">
                  Creative Tim
              </a>
            </li>
          </ul>
        </Container>
        <Container fluid>
          <h2>Resources</h2>
          <ul>
            <li>
              <a href="https://en.wikipedia.org/wiki/Manfred_Max-Neef's_Fundamental_human_needs">
                Manfred Max-Neef's Fundamental human needs
              </a>
            </li>
            <li>
              <a href="https://shop.oogaboogastore.com/products/meenadchi-decolonizing-non-violent-communication">
                meenadchi: Decolonizing Non-Violent Communication
              </a>
            </li>
            <li>
              <a href="https://www.collectivelyfree.org/nonviolent-communication-privileged/">
                Nonviolent Communication is for the privileged by Raffi Marhaba
              </a>
            </li>
            <li>
              <a href="https://www.reddit.com/r/NVC/">
                Reddit NVC
              </a>
            </li>
            <li>
              <a href="https://www.cnvc.org/">
                Center for NVC
              </a>
            </li>
          </ul>
        </Container>
      </div>
    </>
  );
};
