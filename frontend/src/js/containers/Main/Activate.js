import React from "react";
import { connect } from 'react-redux';
import { Verification } from '../../actions/userActions'

@connect((store) => {
  return {
    discover: store.games.discover,
  }
})
class Activate extends React.Component {
  componentDidMount() {
    const key=this.props.match.params.key;
    Verification(key)
        .then((res)=>{
          console.log(res.data)
        });

  }


  render() {
    return (
        <div>fuck you, please login</div>
    )
  }
}


export default Activate;


// onRowClick: function(row, columnIndex, rowIndex) {
//   console.log(this)
//   console.log(row)
//   console.log(`You click row id: ${row.game_name}, column index: ${columnIndex}, row index: ${rowIndex}`);
//   this.props.history.push(`/results/${row.game_id}`);
// },