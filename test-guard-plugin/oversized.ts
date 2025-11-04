// Line 1, 2, 3
function func1() { return 1; }

// Line 4, 5, 6
function func2() { return 2; }

// Line 7, 8, 9
function func3() { return 3; }

//... (continuing for 801 lines total)
// This is a test file with 801 lines to trigger the Code Quality Guardian
// Line count: 801
// Expected: Should be blocked as it exceeds the 800 line threshold for .ts files
