class Array
	def method_missing(method, *args)
		method = method.to_s
		#usability method for select_first without interval
		if method.to_s =~ /^select_first_where_(.*)_is?$/
			symbol = $1.to_sym
			
			self.class.send(:define_method, method){|args| return select_first(symbol => args)}
			return send(method, args.first)
		#usability method for select_first with interval
		elsif method =~ /^select_first_where_(.*)_is_in?$/
			symbol = $1.to_sym
			
			self.class.send(:define_method, method){|minValue, maxValue| 
				return select_first(:name => symbol, :interval => {:min => minValue, :max => maxValue })
			}
			return send(method, args.first, args.last)
			
		#usability method for select_all without interval
		elsif method.to_s =~ /^select_all_where_(.*)_is?$/
			symbol = $1.to_sym
			
			self.class.send(:define_method, method){|args| return select_all(symbol => args)}
			return send(method, args.first)
			
		#usability method for select_all without interval
		elsif method.to_s =~ /^select_all_where_(.*)_is(_in)?$/
			symbol = $1.to_sym
			
			self.class.send(:define_method, method){|minValue, maxValue| 
				return select_all(:name => symbol, :interval => {:min => minValue, :max => maxValue })
			}
			return send(method, args.first, args.last)
		else
			puts "Unsupported method: #{method} with args: #{args.join(', ')}"
		end
	end

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
	
	#select_first help function
	def get_first(**args)	
		key, value = args.first		
		if value.class == Array
			return self.find{ |e| value.include?(e.send(key))}			
		else
			return self.find{ |e| e.send(key) == value}		
		end
	end
	
	#select_first help function
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
	
	#select_all help function
	def get_all(**args)
		key, value = args.first
		if value.class == Array
			return self.find_all{ |e| value.include?(e.send(key))}			
		else
			return self.find_all{ |e| e.send(key) == value}		
		end	
	end
	
	#select_all help function
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



