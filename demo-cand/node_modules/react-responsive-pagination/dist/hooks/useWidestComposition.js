import { useCallback, useState } from 'react';
import { useAvailableWidth } from './useAvailableWidth.js';
import { useFoutDetector } from './useFoutDetector.js';
import { useWidthCalculator } from './useWidthCalculator.js';
import { iteratorNext, lastWhere } from '../helpers/iterator.js';
export function useWidestComposition(narrowToWideCompositionsProvider, maxWidth) {
    const { widthCalculator, metricsRender, clearCache } = useWidthCalculator();
    const foutDetectorRef = useFoutDetector(getItemsDomElements, clearCache);
    const { width = 0, ref: availableWidthRef } = useAvailableWidth(maxWidth);
    const ref = useCallback((element) => {
        foutDetectorRef.current = element;
        availableWidthRef?.(element);
    }, [foutDetectorRef, availableWidthRef]);
    const [showPlaceholder, setShowPlaceholder] = useState(true);
    if (showPlaceholder) {
        const firstComposition = iteratorNext(narrowToWideCompositionsProvider());
        return {
            visible: false,
            items: firstComposition ?? [],
            ref(containerElement) {
                setShowPlaceholder(false);
                ref(containerElement);
            },
            clearCache,
        };
    }
    if (metricsRender) {
        return {
            visible: false,
            items: metricsRender.items,
            ref(containerElement) {
                metricsRender.ref(containerElement);
                ref(containerElement);
            },
            clearCache,
        };
    }
    return {
        visible: true,
        items: getLargestFittingCompositionWithFallback(narrowToWideCompositionsProvider, widthCalculator, width),
        ref,
        clearCache,
    };
}
function getLargestFittingCompositionWithFallback(getNarrowToWideCompositions, getCompositionWidth, maxWidth) {
    const narrowToWideCompositions = getNarrowToWideCompositions();
    const firstComposition = iteratorNext(narrowToWideCompositions) ?? [];
    const doesCompositionFit = (composition) => getCompositionWidth(composition) < maxWidth;
    return lastWhere(narrowToWideCompositions, doesCompositionFit) ?? firstComposition;
}
function getItemsDomElements(viewDomElement) {
    return viewDomElement && Array.from(viewDomElement.children);
}
