import React, { FC } from 'react';
import { Card } from 'react-bootstrap';

interface Props {
  title: string
  titleIcon: string
  stat: string | number
  footer: string
  footerIcon: string
}

export const StatsCard: FC<Props> = (props: Props) => {
  return (
    <>
      <Card className="card-stats">
        <Card.Header className="card-header-warning card-header-icon">
          <div className="card-icon">
            <i className="material-icons">{props.titleIcon}</i>
          </div>
          <p className="card-category">{props.title}</p>
          <h3 className="card-title">45</h3>
        </Card.Header>
        <Card.Footer>
          <div className="stats">
            <i className="material-icons">{props.footerIcon}</i>
            {props.footer}
          </div>
        </Card.Footer>
      </Card>
    </>
  );
}
