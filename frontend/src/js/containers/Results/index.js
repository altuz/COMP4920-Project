import React from "react";
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


@connect((store) => {
  return {
    results: store.games.results,
    keywords:store.games.keywords,
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
    const { keywords } = this.props;
    return(
      <div>
        <h2 style={{'textAlign':'center'}}>Search Result for</h2>
        <div>
        <h4>
          <div><strong>keyword :</strong> {keywords.q} </div>
          <div><strong>genres: </strong> {keywords.genre} </div>
          <div><strong>category: </strong> {keywords.category}  </div>
        </h4>
        </div>
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
