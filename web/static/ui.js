function seizure(i){
    i = (i === undefined) ? 30 : i;
    fetch('/api/brightness/' + 100 * (i % 2)).then(function() {
        if (i > 0) seizure(i - 1);
    });
}
