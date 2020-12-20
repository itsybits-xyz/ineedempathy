import React, { FC } from 'react';

interface Props {
  title: string
  subTitle: string | null
  headers: string[]
  data: (string|number|React.ReactElement|null|undefined)[][]
}

export const Table: FC<Props> = (props: Props) => {
  const tableHeader = props.headers.map((header, idx) => 
    <th>{header}</th>
  );
  const tableRows = props.data.map((row, ridx) => 
    <tr>
      {row.map((col, cidx) => <td>{col ?? ''}</td>)}
    </tr>
  );
  return (
    <>
      <div className="card">
        <div className="card-header card-header-primary">
          <h4 className="card-title ">{props.title}</h4>
          {props.subTitle && <p className="card-category">{props.subTitle}</p>}
        </div>
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead className="text-primary">
                <tr>
                  {tableHeader}
                </tr>
              </thead>
              <tbody>
                {tableRows}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};
