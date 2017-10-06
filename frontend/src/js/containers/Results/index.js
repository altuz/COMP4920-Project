import React from "react";
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
    super(props)
    this.state = {
      results:this.props.location.state,
    }
  }

  imageFormatter(cell,row){
    return (
        <img style={{height:35}} src={cell}/>
    )
  };

  render() {
    console.log(this)
    return(
      <div>
        <BootstrapTable data={this.state.results} options={ option } hover pagination>
        <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
        <TableHeaderColumn isKey dataField='game_name' >Game Name</TableHeaderColumn>
        </BootstrapTable>
      </div>

    );
  }
}

{/*<TableHeaderColumn dataField='price'>Product Price</TableHeaderColumn>*/}
