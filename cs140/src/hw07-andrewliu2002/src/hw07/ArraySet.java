package hw07;

import java.util.Collection;
import java.util.Iterator;
import java.util.Set;

public class ArraySet implements Set<Integer> {
	private int[] array;
	private int used;
	private static final int MAXSIZE=32;
	@Override
	public int size() {
		// TODO Auto-generated method stub
		return used;
	}

	@Override
	public boolean isEmpty() {
		// TODO Auto-generated method stub
		if(used == 0) {
			return true;
		}
		return false;
	}

	@Override
	public boolean contains(Object o) {
		// TODO Auto-generated method stub
		if(o instanceof Integer) {
			int temp = (int) o;
			for( int x: array) {
				if(x==temp) {
					return true;
				}
			}
		}
		return false;
	}

	@Override
	public Iterator<Integer> iterator() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException("Iterators are too complicated for now");
	}

	@Override
	public Object[] toArray() {
		// TODO Auto-generated method stub
		Integer[] vArray = new Integer[used];
		for(int i = 0; i < used; i++) {
			vArray[i] = array[i];
		}
		
		//int vArray = array;
		return vArray;
	}

	@Override
	public <T> T[] toArray(T[] a) {
		throw new UnsupportedOperationException("Generic arrays are too complicated for now.");
	}

	@Override
	public boolean add(Integer e) {	//still need to do
		// TODO Auto-generated method stub
		if(contains(e)) {
			return false;
		}
		if(used != MAXSIZE){
			throw new IllegalArgumentException("ArraySets can have a maximum of " + MAXSIZE + " elements");
		}
		array[used] = e;
		used++;
		return true;
	}

	@Override
	public boolean remove(Object o) {	// still need to o
		if(o instanceof Integer) {
			for(int i = 0; i < used; i++) {
				if(array[i] == (Integer)o) {
					for(int j = i; j < used; j++) {
						array[j] = array[j+1];
					}
					used--;
					return true;
				}
			}
		}
		return false;
	}

	@Override
	public boolean containsAll(Collection<?> c) {
		// TODO Auto-generated method stub
		for(Object val: c) {
			if(!contains(val)) {
				return false;
			}
		}
		return true;
	}

	@Override
	public boolean addAll(Collection<? extends Integer> c) {
		// TODO Auto-generated method stub
		for(Object val: c) {
			if(!add((Integer)val)) {
				return false;
			}
		}
		return true;
	}

	@Override
	public boolean retainAll(Collection<?> c) {
		// TODO Auto-generated method stub
		boolean temp = false;
		for(int i = 0; i < used; i++) {
			if(!c.contains(array[i])) {
				temp = true;
				remove(array[i]);
				used--;
			}
		}
		return temp;
	}

	@Override
	public boolean removeAll(Collection<?> c) {
		boolean remove = false;
		for(Object val : c) {
			if(remove(val)) {
				remove = true;
			}
		}
		return remove;
	}

	@Override
	public void clear() {
		// TODO Auto-generated method stub
		used = 0;
	}
	public String toString() {
		String vStr = "ArraySet {";
		int vTest = used -1 ;
		for(int i = 0; i < used; i++) {
			vStr = vStr + "" + array[i];
			if(i<vTest) {
				vStr = vStr +", ";
			}
		}
		vStr = vStr + "}";
		return vStr;
	}
}
