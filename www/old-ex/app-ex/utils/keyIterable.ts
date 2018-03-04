import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'mapToIterable'
})
export class MapToIterable implements PipeTransform {
    transform(map: { [key: string]: any }, ...parameters: any[]) {
        if (!map) {
            return undefined;
        }
        return Object.keys(map)
            .map((key) => ({ 'key': key, 'value': map[key] }));
    }
}

@Pipe({
    name: 'objectSize'
})
export class ObjectSize implements PipeTransform {
    transform(map: { [key: string]: any }, ...parameters: any[]) {
        if (!map) {
            return 0;
        }
        return Object.keys(map).length;
    }
}
