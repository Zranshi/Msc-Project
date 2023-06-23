package main

import (
	"flag"
	"fmt"
	"math"
	"os"
)

var (
	start    int
	end      int
	filePath string
	rev      bool
	d        map[State]bool
)

type State = [9]byte

type Operator struct {
	mapping [3][3]byte
}

func NewOperator(tt, tm, tf, mt, mm, mf, ft, fm, ff byte) Operator {
	return Operator{
		mapping: [3][3]byte{
			{tt, tm, tf},
			{mt, mm, mf},
			{ft, fm, ff},
		},
	}
}

func (op Operator) cal(formmar, latter State) State {
	s := State{}
	for i := 0; i < 9; i++ {
		s[i] = op.mapping[formmar[i]][latter[i]]
	}
	return s
}

func check(op Operator, f *os.File, d map[State]bool) {
	s1 := State{2, 2, 2, 1, 1, 1, 0, 0, 0}
	s2 := State{2, 1, 0, 2, 1, 0, 2, 1, 0}
	d[s1] = true
	d[s2] = true
	que := []State{s1, s2}
	for len(que) != 0 {
		s := que[0]
		new := make(map[State]bool, 3)
		que = que[1:]
		res := op.cal(s, s)
		if _, ok := d[res]; !ok {
			new[res] = true
		}
		for v := range d {
			res = op.cal(s, v)
			if _, ok := d[res]; !ok {
				new[res] = true
			}
			res = op.cal(v, s)
			if _, ok := d[res]; !ok {
				new[res] = true
			}
		}
		for v := range new {
			d[v] = true
			que = append(que, v)
		}
		if len(d) == 19683 {
			break
		}
	}
	f.WriteString(fmt.Sprintf("%d |", op.mapping))
	f.WriteString(fmt.Sprintln(len(d)))
	for i := range d {
		delete(d, i)
	}
}

func full_arrangement() []State {
	elements := []byte{0, 1, 2}
	totalPossibilities := int(math.Pow(float64(len(elements)), 9))
	possibilities := make([]State, totalPossibilities)
	for i := 0; i < totalPossibilities; i++ {
		possibility := State{}
		for j := 0; j < 9; j++ {
			possibility[j] = elements[i/int(math.Pow(float64(len(elements)), float64(j)))%len(elements)]
		}
		possibilities[i] = possibility
	}
	return possibilities
}

func getFlag() {
	flag.IntVar(&start, "s", 0, "")
	flag.IntVar(&end, "e", 19683, "")
	flag.StringVar(&filePath, "p", "./output", "")
	flag.BoolVar(&rev, "rev", false, "")
	flag.Parse()
}

func main() {
	d = make(map[State]bool, 19683)
	getFlag()
	idx := start
	file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	arrangements := full_arrangement()
	if rev {
		for i, j := 0, len(arrangements); i < j; {
			arrangements[i], arrangements[j] = arrangements[j], arrangements[i]
			i++
			j--
		}
	}
	for _, v := range arrangements[start:end] {
		file.WriteString(fmt.Sprintf("%d / %d |", idx, 19683))
		check(NewOperator(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]), file, d)
		idx++
	}
}
