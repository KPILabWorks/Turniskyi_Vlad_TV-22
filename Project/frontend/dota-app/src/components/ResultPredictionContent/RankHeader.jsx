import rank_1 from '../../assets/rank_1.png';
import rank_2 from '../../assets/rank_2.png';
import rank_3 from '../../assets/rank_3.png';
import rank_4 from '../../assets/rank_4.png';
import rank_5 from '../../assets/rank_5.png';
import rank_6 from '../../assets/rank_6.png';
import rank_7 from '../../assets/rank_7.png';
import rank_8 from '../../assets/rank_8.png';
import { Rank } from '../../enums/Rank.js';

function RankHeader ({rank, setRank}) {
    return(
        
        <div className="flex  flex-col  py-4 ">
            <p className='text-2xl mb-2 font-semibold'>RANK TIER</p>
            {/* <ul className="flex justify-center flex-wrap gap-2 border p-2 rounded mt-2 w-full"> */}
            <ul className="flex content-center justify-center border border-yellow-950 border-2 rounded-sm p-1 bg-yellow-800"> 
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.HERALD ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.HERALD)}
                    >
                        <img className='w-[52px]' src={rank_1} alt="1" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.GUARDIAN ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.GUARDIAN)}
                    >
                        <img className='w-[52px]' src={rank_2} alt="2" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.CRUSADER ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.CRUSADER)}
                    >
                        <img className='w-[52px]' src={rank_3} alt="3" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.ARCHON ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.ARCHON)}
                    >
                        <img className='w-[52px]' src={rank_4} alt="4" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.LEGEND ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.LEGEND)}
                    >
                        <img className='w-[52px]' src={rank_5} alt="5" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.ANCIENT ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.ANCIENT)}
                    >
                        <img className='w-[52px]' src={rank_6} alt="6" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.DIVINE ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.DIVINE)}
                    >
                        <img className='w-[52px]' src={rank_7} alt="7" />
                </li>
                <li className={'content-center m-1 rounded '
                    + (rank === Rank.TITAN ? "bg-yellow-950 " : "hover:bg-yellow-900 hover:cursor-pointer")
                    }
                    onClick={() => setRank(Rank.TITAN)}
                    >
                        <img className='w-[52px]' src={rank_8} alt="8" />
                </li>
            </ul>
        </div>
    );
}
export default RankHeader