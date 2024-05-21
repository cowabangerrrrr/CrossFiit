const fs = require('fs');

function doSuffixArray(s, L = 256) {
    const n = s.length;
    let a = new Array(n).fill(0);
    let b = new Array(Math.max(L, n)).fill(0);
    let col = new Array(n).fill(0);

    for (let char of s) {
        b[char.charCodeAt(0)]++;
    }

    let sum = 0;
    for (let i = 0; i < L; i++) {
        sum += b[i];
        b[i] = sum - b[i];
    }

    for (let i = 0; i < n; i++) {
        a[b[s[i].charCodeAt(0)]] = i;
        b[s[i].charCodeAt(0)]++;
    }

    for (let i = 1; i < n; i++) {
        col[a[i]] = col[a[i - 1]] + (s[a[i - 1]] !== s[a[i]] ? 1 : 0);
    }

    let num = col[a[n - 1]] + 1;
    let buf = new Array(n).fill(0);

    for (let l = 1; l < n; l *= 2) {
        b = new Array(num).fill(0);
        for (let i = 0; i < n; i++) {
            b[col[i]]++;
        }

        sum = 0;
        for (let i = 0; i < num; i++) {
            sum += b[i];
            b[i] = sum - b[i];
        }

        for (let i = 0; i < n; i++) {
            let ns = a[i] - l;
            if (ns < 0) ns += n;
            buf[b[col[ns]]] = ns;
            b[col[ns]]++;
        }

        [a, buf] = [buf, a];

        buf[a[0]] = 0;
        for (let i = 1; i < n; i++) {
            let ns1 = (a[i] + l) % n;
            let ns2 = (a[i - 1] + l) % n;
            let different = (col[a[i]] !== col[a[i - 1]]) || (col[ns1] !== col[ns2]);
            buf[a[i]] = buf[a[i - 1]] + (different ? 1 : 0);
        }

        [col, buf] = [buf, col];
        num = col[a[n - 1]] + 1;
    }

    return a;
}

fs.readFile('suffarray.in', 'utf8', (err, data) => {
    if (err) throw err;
    let s = data.trim();
    s += String.fromCharCode(0);
    let a = doSuffixArray(s).map(i => i + 1);
    fs.writeFile('suffarray.out', a.slice(1).join(' '), (err) => {
        if (err) throw err;
    });
});
