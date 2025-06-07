import { ContentType } from '../enums/ContentType.js';
import MetaContent from "./MetaContent/MetaContent.jsx"
import ResultPredictionContent from "./ResultPredictionContent/ResultPredictionContent.jsx"
import HeroPredictionContent from "./HeroPredictionContent/HeroPredictionContent.jsx"

function MainContent ({type}) {
    return (
        <div className='flex-grow m-auto bg-yellow-700 items-center mt-8 w-[70%] border border-2 border-black border-solid rounded-xl'>
            {type === ContentType.META && <MetaContent/>}
            {type === ContentType.RESULT && <ResultPredictionContent/>}
            {type === ContentType.HERO &&  <HeroPredictionContent/>}
        </div>
    );
}
export default MainContent