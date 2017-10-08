import React from "react";
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

const option = {
  onRowClick: function(row, columnIndex, rowIndex) {
    console.log(row)
    alert(`You click row id: ${row.game_name}, column index: ${columnIndex}, row index: ${rowIndex}`);
  },
};

@connect((store) => {
  return {
    results: store.games.results,
  }
})
export default class Results extends React.Component {
  constructor (props) {
    super(props);
  }

  imageFormatter(cell,row){
    return (
        <img style={{height:35}} src={cell}/>
    )
  };


  priceFormatter(cell,row){
    if(cell){
      return (
          <div>
            ${cell}
          </div>

      )
    }
    return (
        <div>free</div>
    );
  };

  rateFormatter(cell,row) {
    return (
        <div>
          {cell}%
        </div>
    )
  }

  nameFormatter(cell,row,enumObject, index){
    return (
        <div>
          <Link className='game_name' to ={{
            pathname: `/games/${row.game_id}`,
            state: {index}
          }}>
            {cell}
          </Link>
        </div>
    )

  }

  render() {
    return(
      <div>
        <BootstrapTable data={this.props.results}  hover pagination>
          <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
          <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
          <TableHeaderColumn dataField='publisher' width='200px' >Released By</TableHeaderColumn>
          <TableHeaderColumn dataField='price' dataFormat={this.priceFormatter} width='80px'>Price</TableHeaderColumn>
          <TableHeaderColumn dataField='average_rating' dataFormat={this.rateFormatter}>Rating</TableHeaderColumn>
          <TableHeaderColumn dataField='num_player'>Owners</TableHeaderColumn>
        </BootstrapTable>
      </div>

    );
  }
}

{/*<TableHeaderColumn dataField='price'>Product Price</TableHeaderColumn>*/}
