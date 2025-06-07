import { Heroes } from "../../enums/Heroes";

function getHeroImageById(id) {
  for (const heroKey in Heroes) {
    if (Heroes[heroKey].id === id) {
      return Heroes[heroKey].image;
    }
  }
  console.log(id);
  return null;
}

function HeroTableRow ({hero, index}) {
    return (
        <div key={hero.id} className="grid grid-cols-4 font-semibold gap-2 py-2 mb-2 border-b-1 border-yellow-950">
          <div>{index + 1}</div>
          <div className="flex justify-center items-center"><img className="w-16" src={"/src/assets/heroes/" + getHeroImageById(hero.hero_id)}/></div>
          <div >{hero.matches}</div>
          <div className={(hero.wr >= 50 ?  "text-green-500 text-shadow-sm" : "text-red-600 text-shadow-sm")}>{hero.wr}%</div>
        </div>
    );
}
export default HeroTableRow