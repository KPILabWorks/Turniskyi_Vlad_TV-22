import HeroTableRow from "./HeroTableRow";

function HeroTable ({heroes}) {
    // const heroes = [
    //     { id: 1, name: 'Invoker', matches: 120, winrate: 53 },
    //     { id: 2, name: 'Pudge', matches: 200, winrate: 49 },
    //     { id: 3, name: 'Phantom Assassin', matches: 150, winrate: 57 },
    //     { id: 4, name: 'Crystal Maiden', matches: 180, winrate: 51 },
    //     { id: 2, name: 'Pudge', matches: 200, winrate: 49 },
    //     { id: 3, name: 'Phantom Assassin', matches: 150, winrate: 57 },
    //     { id: 4, name: 'Crystal Maiden', matches: 180, winrate: 51 },
    //     { id: 2, name: 'Pudge', matches: 200, winrate: 49 },
    //     { id: 3, name: 'Phantom Assassin', matches: 150, winrate: 57 },
    //     { id: 4, name: 'Crystal Maiden', matches: 180, winrate: 51 },
    //     { id: 2, name: 'Pudge', matches: 200, winrate: 49 },
    //     { id: 3, name: 'Phantom Assassin', matches: 150, winrate: 57 },
    //     { id: 4, name: 'Crystal Maiden', matches: 180, winrate: 51 },
    // ];
    return (
    <div className="mx-7">
      <div className="grid grid-cols-4 gap-2 font-bold  py-2 mb-2 border border-yellow-950 border-2 rounded-sm bg-yellow-800">
        <div>#</div>
        <div>Герой</div>
        <div>Матчі</div>
        <div>Winrate</div>
      </div>

  <div className="custom-scroll max-h-[30rem] overflow-y-auto pr-2">
      {heroes.map((hero, index) => (
        <HeroTableRow hero={hero} index={index}/>
      ))}
    </div></div>
    );
}
export default HeroTable