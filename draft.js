const readline = require("node:readline");

function calculateZFunction(s) {
    const n = s.length;
    const Z = Array(n).fill(0);
    let left = 0, right = 0, k = 0;

    for (let i = 1; i < n; i++) {
        if (i > right) {
            left = i;
            right = i;
            while (right < n && s[right] === s[right - left]) {
                right++;
            }
            Z[i] = right - left;
            right--;
        } else {
            k = i - left;
            if (Z[k] < right - i + 1) {
                Z[i] = Z[k];
            } else {
                left = i;
                while (right < n && s[right] === s[right - left]) {
                    right++;
                }
                Z[i] = right - left;
                right--;
            }
        }
    }

    return Z;
}

// Прочитать входные данные
const n = parseInt(readline());
const s = readline();

// Вычислить Z-функцию
const Z = calculateZFunction(s);

// Вывести результаты
console.log(Z.join(" "));