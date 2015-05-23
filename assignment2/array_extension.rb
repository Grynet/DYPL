class Array
	def select_first(**args)
		num_args = args.length				
		if num_args == 1
			return get_first(args)
		elsif num_args == 2
			return get_first_interval(args)
		else
			return nil
		end
	end
	
	def get_first(**args)	
		key, value = args.first		
		if value.class == Array
			return self.find{ |e| value.include?(e.send(key))}			
		else
			return self.find{ |e| e.send(key) == value}		
		end
	end
	
	def get_first_interval(**args)		
		function = args[:name]
		interval = args[:interval]
		min = interval.has_key?(:min) ? interval[:min] : nil
		max = interval[:max]
		
		self.each do |e|
			value = e.send(function)
			if !min.nil?
				if value >= min && value <= max
					return e
				end
			else 
				if value <= max
					return e
				end
			end
		end		
		return nil
	end
	
	def select_all(**args)
		num_args = args.length
		if num_args == 1
			return get_all(args)
		elsif num_args == 2
			return get_all_interval(args)
		else
			return nil
		end
	end
	
	def get_all(**args)
		key, value = args.first
		if value.class == Array
			return self.find_all{ |e| value.include?(e.send(key))}			
		else
			return self.find_all{ |e| e.send(key) == value}		
		end	
	end
	
	def get_all_interval(**args)		
		function = args[:name]
		interval = args[:interval]
		min = interval.has_key?(:min) ? interval[:min] : nil
		max = interval[:max]
		results = Array.new
		
		self.each do |e|
			value = e.send(function)
			if !min.nil?
				if value >= min && value <= max
					results.push(e)
				end
			else
				if value <= max
					results.push(e)
				end
			end
		end		
		return results
	end
	
end



