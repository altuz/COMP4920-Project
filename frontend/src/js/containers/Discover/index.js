import React from "react";
import { withRouter } from 'react-router';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { getDiscover } from '../../actions/gamesActions';

@connect((store) => {
  return {
    discover: store.games.discover,
  }
})
class Main extends React.Component {

  componentWillMount() {
    console.log(this.props.discover.length)
    if(this.props.discover.length ===0){
       console.log(this.props.discover.length)
      this.props.dispatch(getDiscover());
    }
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



  rateFormatter(cell,row){
    if(cell){
      return(
          <div>
            {cell}%
          </div>
      )
    }
    return (
        <div>
         No Rating
        </div>
    );
  };

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


    if(this.props.discover.length>0){
      return(
          <div >
            <BootstrapTable data={this.props.discover}  hover pagination>
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
    return null;
  }
}


const HomeRoute = withRouter(Main);
export default HomeRoute;


// onRowClick: function(row, columnIndex, rowIndex) {
//   console.log(this)
//   console.log(row)
//   console.log(`You click row id: ${row.game_name}, column index: ${columnIndex}, row index: ${rowIndex}`);
//   this.props.history.push(`/results/${row.game_id}`);
// },