// Courtesy of https://stackoverflow.com/a/31490738/3030563
function mix(a, b, v)
{
    return (1 - v) * a + v * b;
}

export function HSVtoRGB(H, S, V)
{
    const V2 = V * (1 - S);
    const r  = ((H >= 0 && H <= 60) || (H >= 300 && H <= 360)) ? V : ((H >= 120 && H <= 240) ? V2 : ((H >= 60 && H <= 120) ? mix(V, V2, (H - 60) / 60) : ((H >= 240 && H <= 300) ? mix(V2, V, (H - 240) / 60) : 0)));
    const g  = (H >= 60 && H <= 180) ? V : ((H >= 240 && H <= 360) ? V2 : ((H >= 0 && H <= 60) ? mix(V2, V, H / 60) : ((H >= 180 && H <= 240) ? mix(V, V2, (H - 180) / 60) : 0)));
    const b  = (H >= 0 && H <= 120) ? V2 : ((H >= 180 && H <= 300) ? V : ((H >= 120 && H <= 180) ? mix(V2, V, (H - 120) / 60) : ((H >= 300 && H <= 360) ? mix(V, V2, (H - 300) / 60) : 0)));

    return {
        r : Math.round(r * 255),
        g : Math.round(g * 255),
        b : Math.round(b * 255)
    };
}

export function calcOffset(value: number, min: number, max: number) {
    return((value - min) / (max - min) * 100);
}


// https://stackoverflow.com/questions/442404/retrieve-the-position-x-y-of-an-html-element
export function getOffset(el) {
    let _x = 0;
    let _y = 0;
    while ( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
                _x += el.offsetLeft - el.scrollLeft;
                _y += el.offsetTop - el.scrollTop;
                el = el.offsetParent;
            }
    return { top: _y, left: _x };
}

